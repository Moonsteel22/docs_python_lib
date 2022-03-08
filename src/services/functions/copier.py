import logging
from urllib.error import HTTPError

from docs_python_lib.src.docs_lib.settings.google import GENERATED_CVS_FOLDER
from docs_python_lib.src.services.google_api_auth_service import GoogleApiServices


def template_copy_drive(
    template_id: str,
    services: GoogleApiServices = GoogleApiServices(),
    filename: str = "copy_file",
):
    """
    This function copy file from
    one Google drive by file ID to another
    """
    try:
        result = (
            services.drive_service.files()
            .copy(
                fileId=template_id,
                body={"name": filename, "parents": [GENERATED_CVS_FOLDER]},
            )
            .execute()
        )
        return result["id"]
    except HTTPError as err:
        logging.error(msg=err)
