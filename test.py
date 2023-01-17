from flask import Flask,request,jsonify
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

@app.route('/api',methods=['GET'])

def hello_world():

	import pandas as pd
	d = {}
	d['Soybean_meal_US'] = str(request.args['Soybean_meal_US'])
	d['Crude_Oil'] = str(request.args['Crude_Oil'])
	d['New_Month'] = str(request.args['New_Month'])
	d['Year'] = str(request.args['Year'])
	print(d)
	print(type(d))
	df_input = pd.DataFrame([d])
	print(df_input)
	df_input2 = pd.read_excel('test_input.xlsx')
	print(df_input2)
	df_new = pd.read_excel('dataofPrice_cut.xlsx')

	df_new['New_Month'] = pd.to_datetime(df_new['Date']).dt.strftime('%m')
	df_new['Year'] = pd.to_datetime(df_new['Date']).dt.strftime('%Y')

	df_row = pd.concat([df_new[-10:], df_input], ignore_index=True)

	df_row['New_Month'] = df_row['New_Month'].astype(float)
	df_row['Year'] = df_row['Year'].astype(float)
	df_row = df_row[['Year', 'New_Month', 'Crude_Oil', 'Soybean_meal_US']]
	batch = df_new[['Thai_Import']][-11:]
	x_scaler = MinMaxScaler()
	Predict_scaled_x = x_scaler.fit_transform(df_row)
	Predict_scaled_y = x_scaler.fit_transform(batch)
	len = 1
	rs_generator = TimeseriesGenerator(Predict_scaled_x, Predict_scaled_y, length=len, batch_size=1)
	from keras.models import load_model
	model = load_model('ewan.h5')
	predicted_output = model.predict(rs_generator, batch_size=1)
	predict_concat = pd.concat([pd.DataFrame(predicted_output), pd.DataFrame(Predict_scaled_x[:, 1:][len:])], axis=1)
	predict_trans = x_scaler.inverse_transform(predict_concat)
	df_input['Thai_Import'] = predict_trans[9:10, 0]
	answer = df_input.drop(['Crude_Oil', 'Soybean_meal_US', 'Year', 'New_Month'], axis=1)
	ans = answer.to_dict()
	predict = ans['Thai_Import'][0]
	predict = "{:.2f}".format(round(predict, 2))
	print(predict)
	# print(ans['Thai_Import'])
 ##-------------------------------------------------------------##

	return jsonify(predict)

if __name__ == '__main__':
	app.run()