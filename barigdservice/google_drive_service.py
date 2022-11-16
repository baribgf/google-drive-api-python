"""
## Google Drive Service
A simple tool to manage
Google Drive files
"""

#########################
# Developed by: Bari BGF
# On: Nov 16th, 2022
#########################

import io
import os
import shutil

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

class GoogleDriveService:
	def __init__(self, token_path: str, credentials_path: str = None):
		self.token_path = token_path
		self.credentials_path = credentials_path

	def authorize(self) -> Credentials:
		creds = None
		# If modifying these scopes, delete the file token.json.
		SCOPES = ["https://www.googleapis.com/auth/drive"]
		if os.path.exists(self.token_path):
			creds = Credentials.from_authorized_user_file(
				self.token_path, SCOPES)

		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					self.credentials_path, SCOPES
				)
				creds = flow.run_local_server(port=0)

			with open(self.token_path, "w") as token:
				token.write(creds.to_json())
		return creds

	def read_file(self, file_id: str) -> bytes:
		creds = self.authorize()
		if not creds:
			return None

		drive = build("drive", "v3", credentials=creds)

		try:
			request = drive.files().get_media(fileId=file_id)
			file = io.BytesIO()
			downloader = MediaIoBaseDownload(file, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				print(F'Downloading progress: {int(status.progress() * 100)} . .')

			return file.getvalue()

		except HttpError as err:
			print(f"Error occured: {err}")
			return None

	def upload_file(self, file_path: str, parents: str = None) -> str:
		creds = self.authorize()
		if not creds:
			return None

		drive = build("drive", "v3", credentials=creds)

		try:
			file_name: str = os.path.basename(file_path)
			try:
				shutil.copyfile(file_path, f"./{file_name}")
			except shutil.SameFileError:
				pass
			file_extension = file_name.split(".")[-1]
			file_metadata = {"name": file_name, "parents": (lambda: [parents] if parents else None)()}
			mime_type = "text/plain"
			if file_extension in ["jpg", "png"]:
				mime_type = "image/gif"
			elif file_extension in ["html", "htm"]:
				mime_type = "text/html"
			elif file_extension == "json":
				mime_type = "application/json"

			media = MediaFileUpload(file_name, mimetype=mime_type)

			file = drive.files().create(body=file_metadata, media_body=media).execute()

			os.remove(f"./{file_name}")
			return file.get("id")
		except HttpError as err:
			print(f"Error occured: {err}")
			return None

	def list_files(self, folder_id: str) -> list:
		creds = self.authorize()
		if not creds:
			return None

		drive = build("drive", "v3", credentials=creds)

		try:
			files = []
			page_token = None
			while True:
				response = drive.files().list(
					q = f"'{folder_id}' in parents and trashed = false",
					fields = "nextPageToken, files(id, name)",
					pageToken = page_token
				).execute()
				files.extend(response.get('files', []))
				page_token = response.get('nextPageToken', None)
				if page_token is None:
					break

			return files
		except HttpError as err:
			print(f"Error occured: {err}")
			return []

	def create_folder(self, folder_name: str, parents: str=None) -> str:
		creds = self.authorize()
		if not creds:
			return None

		drive = build("drive", "v3", credentials=creds)

		try:
			file_metadata = {
				"name": folder_name,
				"parents": (lambda: [parents] if parents else None)(),
				"mimeType": 'application/vnd.google-apps.folder'
			}
			folder = drive.files().create(body = file_metadata, fields = 'id').execute()

			return folder.get('id')
		except HttpError as err:
			print(f"Error occured: {err}")
			return None
