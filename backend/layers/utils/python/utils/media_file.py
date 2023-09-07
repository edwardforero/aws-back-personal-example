
LOGO_MEDIA_TYPE = "logo_image"
BACKGROUND_PROFILE_IMAGE = "background_profile_image"
CONFIG_FILES = [BACKGROUND_PROFILE_IMAGE, LOGO_MEDIA_TYPE, "profile_image",]
VIDEO_TYPES = ["video"]
IMAGE_TYPES = ["image",]
VALID_MEDIA_TYPES = IMAGE_TYPES + VIDEO_TYPES

ALL_MEDIA_TYPES = CONFIG_FILES + VALID_MEDIA_TYPES

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "svg", "bmp", ]
VIDEO_EXTENSIONS = ["mp4", "webm", "mov", "avi", "mkv", "wmv"]



def validate_media_file_extension(media_type, file_name):
    extension = file_name.split('.')[-1]
    valid_extensions = "no valid media_type"
    if media_type == LOGO_MEDIA_TYPE or 'image' in media_type:
        valid_extensions = IMAGE_EXTENSIONS
    elif 'video' in media_type:
        valid_extensions = VIDEO_EXTENSIONS
        
    return {"isValid": extension in valid_extensions, "valids": valid_extensions}

def validate_media_type(media_type):
    
    return {
        "isValid": media_type in ALL_MEDIA_TYPES, 
        "valids": ALL_MEDIA_TYPES,
    }

