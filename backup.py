####
# This script demonstrates how to log in to Tableau Server Client.
#
# To run the script, you must have installed Python 3.5 or later.
####

import argparse
import getpass
import os

import tableauserverclient as TSC


def main():
	parser = argparse.ArgumentParser(description='Logs in to the server.')

	parser.add_argument('--server', '-s', required=True, help='server address')
	parser.add_argument('--target', '-t', required=True, help='Folder where the backup will be created')

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--username', '-u', help='username to sign into the server')
	group.add_argument('--token-name', '-n', help='name of the personal access token used to sign into the server')
	parser.add_argument('--sitename', '-S', default='')

	args = parser.parse_args()

	# Make sure we use an updated version of the rest apis.
	server = TSC.Server(args.server, use_server_version=True)

	if args.username:
		# Trying to authenticate using username and password.
		password = getpass.getpass("Password: ")

		print("\nSigning in...\nServer: {}\nSite: {}\nUsername: {}".format(args.server, args.sitename, args.username))
		tableau_auth = TSC.TableauAuth(args.username, password, site_id=args.sitename)
		with server.auth.sign_in(tableau_auth):
			print('Logged in successfully')

	else:
		# Trying to authenticate using personal access tokens.
		personal_access_token = getpass.getpass("Personal Access Token: ")

		print("\nSigning in...\nServer: {}\nSite: {}\nToken name: {}"
			  .format(args.server, args.sitename, args.token_name))
		tableau_auth = TSC.PersonalAccessTokenAuth(token_name=args.token_name,
												   personal_access_token=personal_access_token, site_id=args.sitename)
		with server.auth.sign_in_with_personal_access_token(tableau_auth):
			if not os.path.exists(args.target):
				os.makedirs(args.target)
			print('Logged in successfully')
			all_project_items, pagination_item = server.projects.get()
			for proj in all_project_items:
				if not os.path.exists(args.target + '/' + proj.name):
					os.makedirs(args.target + '/' + proj.name)

			# Download Datasources
			all_datasources, pagination_item = server.datasources.get()
			print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
			print([datasource.name for datasource in all_datasources])
			for datasource in all_datasources:
				file_path = server.datasources.download(datasource.id, filepath=args.target + '/' + datasource.project_name + "/" + datasource.name, include_extract=True)
				print("\nDownloaded the file to {0}.".format(file_path))

			# Download Workbooks
			all_workbooks, pagination_item = server.workbooks.get()
			print("\nThere are {} workbooks on site: ".format(pagination_item.total_available))
			print([workbook.name for workbook in all_workbooks])
			for workbook in all_workbooks:
				file_path = server.workbooks.download(workbook.id, filepath=args.target + '/' + workbook.project_name + "/" + workbook.name, include_extract=True)
				print("\nDownloaded the file to {0}.".format(file_path))

			# Download Flows
			all_flows, pagination_item = server.flows.get()
			print("\nThere are {} flows on site: ".format(pagination_item.total_available))
			print([flow.name for flow in all_flows])
			for flow in all_flows:
				file_path = server.flows.download(flow.id, filepath=args.target + '/' + flow.project_name + "/" + flow.name)
				print("\nDownloaded the file to {0}.".format(file_path))

if __name__ == '__main__':
	main()