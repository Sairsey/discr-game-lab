import emailpy
import json
import os
import logging
import re

logger = logging.getLogger('example_logger')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


params = {
    "email_user": "example@gmail.com",
    "service": "gmail",  # or outlook or yahoo
    "save_dir_name": "mail_saved",
    "password": "123"
}

def proccess_attachment(filename : str, sender_email : str):
    if not filename.endswith("py"):
        logger.error("INVALID FILE WILL BE DELETED")
        os.remove("./attachments/" + filename)
    else:
        new_file_name = sender_email.replace("@", "_").replace(".", "_")
        logger.info("Will save to " + params["save_dir_name"] + "and name " + new_file_name)
        if os.path.exists("./" + params["save_dir_name"] + "/" + new_file_name + ".py"):
            os.remove("./" + params["save_dir_name"] + "/" + new_file_name + ".py")
        os.rename("./attachments/" + filename, "./" + params["save_dir_name"] + "/" + new_file_name + ".py")

# haha C-style programming
def main(fname = "bot.json"):
    global params # because python can do strange things without it... Ugh

    # at first I just load data from json
    with open(fname, "r") as f:
        params.update(json.loads(f.read()))

    if not os.path.exists(params["save_dir_name"]):
        os.mkdir(params["save_dir_name"])

    sm = emailpy.ServiceManager()
    mail = sm.get_service(params["service"])
    mail.setup(params["email_user"], params["password"])

    # main program cycle
    # it has easy idea, and I belive that comments in theese functions is enough
    while True:
        try:
            print('Another attempt to check EMAIL')
            for msg in mail.read(criteria=emailpy.Constants.UNSEEN, download_attachments=True):
                for fn in msg.Attachments:
                    logger.info("Attachment file name: " + fn)
                    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', msg.From)
                    proccess_attachment(fn, match[0])
        except (KeyboardInterrupt):
            break
    logger.info('End of cursed cycle of code gathering')

if __name__ == "__main__":
    main()