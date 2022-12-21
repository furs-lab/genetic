import main
import requests

def send_request(fname):
    analysis_data_json = main.json_from_excel(fname)
    res = requests.get('http://127.0.0.1:5000/results', json=analysis_data_json)
    print("responce ->", res.json())

if __name__ == '__main__':
    send_request("tst_analysis.xlsx")