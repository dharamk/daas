#!/bin/python3

class DeviceImage:
    def __init__(self, blob=None, dev_id=None):
        self.image_id = None
        self.name = None
        self.user_tags = None
        self.dev_id = None
        self.blob_file = None
        pass


class RemoteImageUploader:
    """
    This is a Remote Image Uploader Service.
    For example -  User <--> Server <--> Agent(device)
    User will trigger a request to upload a new image to a device(which he owns/controls/leased)
    Server will accept the request, intimate the agent about the upload, start the upload and return
    the upload status to the user.
    """

    def __init__(self):
        self.pending_uploads = dict()
        self.completed_uploads = dict()
        pass

    def download_image(self, bin_file, dev_id):
        image = DeviceImage(bin_file, dev_id)
        self.pending_uploads.append(image)
        pass

    def stop_download(self, dev_id):
        pass

    def resume_download(self, dev_id):
        pass

