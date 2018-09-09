# from flask import Flask, render_template
# app = Flask(__name__, template_folder='new_html')


# @app.route('/alpha')
# def alpha():
#     return "This is the alpha version"

# @app.route('/beta')
# def beta():
#     return "This is the beta version"

 
# # @app.route('/')
# # def display():
# #     return "Looks like it works!"


# @app.route('/')
# def render():
#     return render_template('index.html')

# if __name__=='__main__':
#     app.run(debug=True)



from __future__ import absolute_import, print_function
from flask import Flask, render_template, request
from pprint import pprint
import unittest
import webbrowser

import docusign_esign as docusign
from docusign_esign import AuthenticationApi, TemplatesApi, EnvelopesApi
from docusign_esign.rest import ApiException


app = Flask(__name__, static_url_path="/new_html", static_folder='/media/harshad/work/pennapps/new_html')
@app.route('/')
def static_file():
    return app.send_static_file('index.html')

@app.route('/input')
def render():
    if 'filename' in request.args:
		user_name = "30c0525d-e78d-4b50-8d1c-ecaaeb951a12"
		integrator_key = "23e1947d-fd87-4a62-95c4-3c2b0f419d53"
		base_url = "https://demo.docusign.net/restapi"
		oauth_base_url = "account-d.docusign.com" # use account.docusign.com for Live/Production
		redirect_uri = "https://www.docusign.com/api"
		private_key_filename = "keys/docusign_private_key.txt"
		user_id = "30c0525d-e78d-4b50-8d1c-ecaaeb951a12"
		template_id = "31edfa30-c5f8-4802-9beb-5978cac10c74"
		myfilename = request.args.get('filename')
		api_client = docusign.ApiClient(base_url)

		# IMPORTANT NOTE:
		# the first time you ask for a JWT access token, you should grant access by making the following call
		# get DocuSign OAuth authorization url:
		# print(api_client)
		# print(integrator_key, redirect_uri,oauth_base_url)
		oauth_login_url = api_client.get_jwt_uri(integrator_key, redirect_uri, oauth_base_url)
		# open DocuSign OAuth authorization url in the browser, login and grant access
		# webbrowser.open_new_tab(oauth_login_url)
		# print(oauth_login_url)

		# END OF NOTE

		# configure the ApiClient to asynchronously get an access token and store it
		# print(private_key_filename)
		api_client.configure_jwt_authorization_flow(private_key_filename, oauth_base_url, integrator_key, user_id, 3600)
		# print("test")
		docusign.configuration.api_client = api_client

		template_role_name = 'client'

		# create an envelope to be signed
		envelope_definition = docusign.EnvelopeDefinition()
		envelope_definition.email_subject = 'Please Sign my Python SDK Envelope'
		envelope_definition.email_blurb = 'Hello, Please sign my Python SDK Envelope.'
		print(envelope_definition)

		# assign template information including ID and role(s)
		envelope_definition.template_id = template_id

		# create a template role with a valid template_id and role_name and assign signer info
		t_role = docusign.TemplateRole()
		t_role.role_name = template_role_name
		t_role.name ='Pat Developer'
		t_role.email = "%(filename)s"

		# # create a list of template roles and add our newly created role
		# # assign template role(s) to the envelope
		envelope_definition.template_roles = [t_role]

		# # send the envelope by setting |status| to "sent". To save as a draft set to "created"
		envelope_definition.status = 'sent'

		auth_api = AuthenticationApi()
		envelopes_api = EnvelopesApi()

		try:
		    login_info = auth_api.login(api_password='true', include_account_id_guid='true')
		    assert login_info is not None
		    assert len(login_info.login_accounts) > 0
		    login_accounts = login_info.login_accounts
		    assert login_accounts[0].account_id is not None

		    base_url, _ = login_accounts[0].base_url.split('/v2')
		    api_client.host = base_url
		    docusign.configuration.api_client = api_client

		    envelope_summary = envelopes_api.create_envelope(login_accounts[0].account_id, envelope_definition=envelope_definition)
		    assert envelope_summary is not None
		    assert envelope_summary.envelope_id is not None
		    assert envelope_summary.status == 'sent'

		    # print("EnvelopeSummary: ", end="")
		    # pprint(envelope_summary)

		except ApiException as e:
		    print("\nException when calling DocuSign API: %s" % e)
		    assert e is None # make the test case fail in case of an API exception

		    return app.send_static_file('index.html', envelope_summary)
		else:
		    return app.send_static_file('index.html')

# def docusign_call():
	

if __name__ == "__main__":
    app.run()