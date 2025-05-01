import streamlit as st
from langgraph.graph import StateGraph
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub
from langchain_community.chat_models import ChatCohere
from typing import TypedDict
import datetime
import requests

# Exchange rate INR to USD
EXCHANGE_RATE_INR_TO_USD = 1 / 82

def convert_to_usd(inr_amount: float) -> float:
    return inr_amount * EXCHANGE_RATE_INR_TO_USD

# Geocoding with OpenStreetMap (Nominatim)
def get_coordinates(city_name: str):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    headers = {"User-Agent": "TravelPlannerApp"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

# Flight data using OpenSky Network (REST API version)
def search_flights(destination: str, budget_inr: float) -> str:
    lat, lon = get_coordinates(destination)
    if lat is None or lon is None:
        return f"Could not find coordinates for {destination}."

    # Define bounding box
    lamin = lat - 1
    lamax = lat + 1
    lomin = lon - 1
    lomax = lon + 1

    # OpenSky REST API call
    opensky_url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lamax={lamax}&lomin={lomin}&lomax={lomax}"
    headers = {"User-Agent": "TravelPlannerApp"}
    try:
        response = requests.get(opensky_url, headers=headers, timeout=10)
        data = response.json()
    except Exception as e:
        return f"Error contacting OpenSky API: {e}"

    if not data.get("states"):
        return f"No live flights found near {destination} at the moment."

    result = f"Live flights near {destination}:\n"
    for state in data["states"][:5]:  # limit to 5 results
        callsign = state[1].strip() if state[1] else "N/A"
        altitude = state[7] if state[7] else "N/A"
        velocity = state[9] if state[9] else "N/A"
        result += f"- Callsign: {callsign}, Altitude: {altitude} m, Velocity: {velocity} m/s\n"

    estimated_flight_cost = min(budget_inr * 0.4, 55000)
    result += f"\nEstimated round-trip fare: ₹{estimated_flight_cost:.2f} (approx)"
    return result

def search_hotels(destination: str, budget_inr: float) -> str:
    budget_usd = convert_to_usd(budget_inr)
    hotel_cost_usd = 150 * (budget_usd / 500)
    hotel_cost_inr = hotel_cost_usd * 82
    return f"Hotel found in {destination} for ₹{hotel_cost_inr:.2f}/night."

def get_weather(destination: str) -> str:
    return f"Weather in {destination} is sunny and 25°C."

def suggest_events(destination: str) -> str:
    return f"Events in {destination}: Art Festival, Food Market."

# Define tools
tools = [
    Tool(name="FlightSearchTool", func=search_flights, description="Search flights to a destination"),
    Tool(name="HotelSearchTool", func=search_hotels, description="Search hotels at a destination"),
    Tool(name="WeatherTool", func=get_weather, description="Get weather for a destination"),
    Tool(name="EventSuggestor", func=suggest_events, description="Suggest local events in a destination")
]

# ReAct + LangGraph setup
prompt = hub.pull("hwchase17/react")
llm = ChatCohere(cohere_api_key="COHERE API LEY")  # replace with your real key
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=2, handle_parsing_errors=True)

class TravelPlannerState(TypedDict):
    input: str
    output: str

builder = StateGraph(TravelPlannerState)
builder.add_node("Planner", agent_executor)
builder.set_entry_point("Planner")
builder.set_finish_point("Planner")
graph = builder.compile()

# Streamlit UI
st.title("AI-Powered Travel Itinerary Planner")

st.write("Enter your travel details and get a realistic plan powered by LangGraph, OpenSky API, and OpenStreetMap!")

destination = st.text_input("Destination", "Paris")
trip_duration = st.number_input("Trip Duration (in days)", min_value=1, max_value=30, value=7)
departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")
budget_inr = st.slider("Budget (in INR)", min_value=5000, max_value=500000, value=150000, step=1000)

if st.button("Generate Itinerary"):
    with st.spinner('Generating itinerary...'):
        user_input = f"Plan a trip to {destination} for {trip_duration} days, departing on {departure_date} and returning on {return_date}. The budget is ₹{budget_inr}."
        output = graph.invoke({"input": user_input})

    st.subheader("Suggested Itinerary")
    st.write(output)
    st.markdown(f"""
    **Destination:** {destination}  
    **Trip Duration:** {trip_duration} days  
    **Departure Date:** {departure_date}  
    **Return Date:** {return_date}  
    **Budget:** ₹{budget_inr}
    """)
