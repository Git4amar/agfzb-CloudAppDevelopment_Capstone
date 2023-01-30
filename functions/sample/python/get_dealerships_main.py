"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException


def main(params):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        List of all databases in instance
    """
    # service = CloudantV1(authenticator=IAMAuthenticator(creds["IAM_API_KEY"]))
    service = CloudantV1(authenticator=IAMAuthenticator(params["IAM_API_KEY"]))

    print(service.get_authenticator())
    # service.set_service_url(creds["CLOUDANT_URL"])
    service.set_service_url(params["CLOUDANT_URL"])

    try:
        response = service.post_find(
            db="dealerships", selector={"$or": [{"state": "Texas"}, {"st": "CA"}]}
        ).get_result()
        # print(response)
    except ApiException as err:
        print("ERROR", err)
    else:
        return response


#if __name__ == "__main__":
#    main()
