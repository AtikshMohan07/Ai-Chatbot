
import openai
import pandas as pd
from sk import my_sk
from filepath import order_file_path

# Set your OpenAI API key

openai.api_key = my_sk

# Load Amazon data
def load_amazon_data(order_file_path):
    odf = pd.read_csv(order_file_path)
    return odf

odf = load_amazon_data(order_file_path)


def analyze_spending(odf):
    product = odf['Title']
    product_spending = odf.groupby('OurPrice')['Title'].sum()
    return product, product_spending

sp = analyze_spending(odf)

def get_purchase_insights(odf):
    product, product_spending = analyze_spending(odf)
    insights = {
        "product": product,
        "product_spending": product_spending
    }
    return insights

insights = get_purchase_insights(odf)


def get_openai_response(prompt):
    Myresponse = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         messages=[{"role": "user", "content": prompt}]
    )
    return Myresponse





if __name__ == "__main__":
    while True:
        print("some sample questions as below\n")
        print('''
                which book is sold most?
                Give me list of all the publishers?
                which country has purchased more books?
              ''')
        rqst = input("Enter your request \n")
        ai = get_openai_response(rqst)
        print(ai.choices[0].message.content)
        choice = input("Do you whish to continue? \n")
        if choice in ("Y", "y", "yes", "YES"):
            continue
        else:
            break
