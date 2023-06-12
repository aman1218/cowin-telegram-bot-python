import requests
import datetime
import time

while(1):
	base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
	today_date = datetime.date.today()
	today_date = today_date.strftime('%d-%m-%Y')
	tom_date = datetime.date.today() + datetime.timedelta(days=1)
	tom_date = tom_date.strftime('%d-%m-%Y')
	group_id = "-1001159182149"
	api_url_telegram = "https://api.telegram.org/{bot-api-id}/sendMessage?chat_id=group_id&text="
	wb_district_ids = [144]
	dates = [ today_date , tom_date ]

	def fetch_data_from_cowin(district_id, x):
		query_params = "?district_id={}&date={}".format(district_id, x)
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		final_url = base_cowin_url+query_params
		response = requests.get(final_url, headers=headers)
		extract_availability_data(response)
		# print(response.text)


	def fetch_data_for_state(district_ids):
		for district_id in district_ids:
			for x in dates:
				if x!=2:
					fetch_data_from_cowin(district_id, x)

	def extract_availability_data(response):
		response_json = response.json()
		for session in response_json["sessions"]:
				if session["available_capacity_dose1"] > 0 and session["min_age_limit"]>=18 or session["available_capacity_dose2"] > 0:
					message = "Pincode: {},\nName: {},\nDose1: {},\nDose2: {},\nMinimum Age: {},\nAddress: {},\nFee Type: {},\nCost: {},\nVaccine Type: {},\nDate: {}".format(
						session["pincode"], session["name"], 
						session["available_capacity_dose1"],
         					session["available_capacity_dose2"],
						session["min_age_limit"], session ["address"], session ["fee_type"], session ["fee"], session ["vaccine"], session["date"]
					)
					send_message_telegram(message)

	def send_message_telegram(message):
		final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
		final_telegram_url = final_telegram_url + message
		response = requests.get(final_telegram_url)
		print(response)


	if __name__ == "__main__":
		fetch_data_for_state(wb_district_ids)
	time.sleep(300)
