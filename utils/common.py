from utils.constants import UPLOAD_FOLDER, DOMAIN_NAME


def gen_image_url(booth_id, image_name):
    return "http://{}/{}/{}/{}".format(DOMAIN_NAME, UPLOAD_FOLDER, booth_id, image_name)
