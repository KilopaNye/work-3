from flask import *
from datetime import *
import mysql.connector
from dotenv import *
import boto3
import uuid
import os

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
AWS_S3_REGION = os.getenv('AWS_S3_REGION')
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv('host')

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=AWS_S3_REGION)

app = Flask(__name__, static_folder="public")
app.secret_key = "WGXaTKE7JR9MzzykHVp1O8ix7cnkx5eOb400I5gPxXJI3I8saAUWZjDLxs6056M"
cnxpool = mysql.connector.pooling.MySQLConnectionPool(user=user, password=password, host=host, database="board",pool_name="mypool",pool_size=5)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.json.ensure_ascii = False

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/upload",methods=["POST"])
def upload_file_to_s3():
	try:
		message = request.form['message']
		print(message)
		file = request.files['file']
		filename = str(uuid.uuid4())+".jpeg"
		try:
			con = cnxpool.get_connection()
			cursor = con.cursor(dictionary=True)
			s3.upload_fileobj(file, AWS_S3_BUCKET, filename, ExtraArgs={'ContentType': "image/jpeg"})
			cursor.execute('INSERT INTO messages(message,image_id) VALUE(%s,%s)',(message, filename,))
			con.commit()
			return jsonify({'message': 'File uploaded to S3 successfully'})
		except Exception as err:
			print(err)
			return jsonify({'message': f'Error: {str(err)}'})
		finally:
			cursor.close()
			con.close()

	except Exception as err:
		con = cnxpool.get_connection()
		cursor = con.cursor(dictionary=True)
		message = request.form.get('message')
		cursor.execute('INSERT INTO messages(message) VALUE(%s)',(message,))
		con.commit()
		return jsonify({'message': f'Error: {str(err)}'})

@app.route("/api/loading",methods=["GET"])
def loading_message():
	try:
		con = cnxpool.get_connection()
		cursor = con.cursor(dictionary=True)
		cursor.execute('SELECT * FROM messages ORDER BY time DESC')
		data = cursor.fetchall()
		print(data)
		return jsonify({"data":data})
	except Exception as err:
		return jsonify({'error':True,'message':str(err)})
	finally:
			cursor.close()
			con.close()
app.run(host="0.0.0.0", port=3600, debug=True)