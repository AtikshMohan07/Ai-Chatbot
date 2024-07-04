
import openai
import pandas as pd

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Load Amazon data
def load_amazon_data(file_path):
    df = pd.read_csv(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year-Month'] = df['Order Date'].dt.to_period('M')
    return df

# Analyze spending patterns
def analyze_spending(df):
    total_spending = df['Item Total'].sum()
    monthly_spending = df.groupby('Year-Month')['Item Total'].sum()
    return total_spending, monthly_spending

# Identify impulse buys (simplified example rule)
def identify_impulse_buys(df):
    df['Impulse Buy'] = df['Time to Purchase'].apply(lambda x: x < pd.Timedelta(minutes=10))
    impulse_buys = df[df['Impulse Buy']]
    return impulse_buys

# Get purchase insights
def get_purchase_insights(df):
    total_spending, monthly_spending = analyze_spending(df)
    impulse_buys = identify_impulse_buys(df)
    insights = {
        "total_spending": total_spending,
        "monthly_spending": monthly_spending,
        "impulse_buys": impulse_buys
    }
    return insights

# Function to get OpenAI GPT-3 response
def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Chatbot function
def chatbot(file_path, user_question):
    df = load_amazon_data(file_path)
    insights = get_purchase_insights(df)
    
    # Generate a prompt for OpenAI API
    prompt = f"""
    You are an AI assistant analyzing Amazon purchase data for a user. The user has provided their purchase data.
    
    Total spending: ${insights['total_spending']}
    
    Monthly spending:
    {insights['monthly_spending']}
    
    Impulse buys:
    {insights['impulse_buys']}
    
    The user asks: "{user_question}"
    Based on the data, provide insights and guidance on future purchases.
    """
    
    # Get response from OpenAI API
    response = get_openai_response(prompt)
    return response

# Example usage
file_path = 'amazon_order_history.csv'
user_question = "Should I buy a new laptop this month?"
response = chatbot(file_path, user_question)
print(response)
