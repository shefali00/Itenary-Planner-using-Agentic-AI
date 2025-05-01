
# AI-Powered Travel Itinerary Planner

An AI-powered travel itinerary planner that leverages **LangGraph**, **OpenSky API**, **OpenStreetMap**, and **ChatCohere** to generate personalized travel plans. The app analyzes user input regarding destination, budget, and preferences to suggest flights, hotels, weather, and local events.

## Features

- **Dynamic Trip Planning**: Allows users to enter travel details and generates a complete itinerary with flight, hotel, weather, and event suggestions.
- **Flight Data**: Uses the OpenSky API to fetch live flight data and estimates the cost based on the user's budget.
- **Hotel Recommendations**: Suggests hotels based on the user's budget for the destination.
- **Weather Information**: Provides current weather data for the destination city.
- **Event Suggestions**: Recommends local events like festivals and markets.
- **Interactive UI**: Built with **Streamlit**, offering a user-friendly interface to input data and receive results.

## Requirements

1. **Python** (v3.7 or higher)
2. **Cohere API Key** (for ChatCohere)
3. **Streamlit**
4. **LangChain**
5. **LangGraph**
6. **OpenSky API**
7. **OpenStreetMap**

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/ai-travel-itinerary-planner.git
cd ai-travel-itinerary-planner
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Cohere API Key

- Sign up for **Cohere** and get your API key from [Cohere](https://cohere.ai/).
- Add the key to the code in `app.py`:
  
```python
llm = ChatCohere(cohere_api_key="your-cohere-api-key")
```

### 5. Run the Application

```bash
streamlit run app.py
```

### 6. Enter Your Travel Details

- **Destination**: Enter the city you wish to travel to.
- **Trip Duration**: Specify the number of days for your trip.
- **Departure Date & Return Date**: Choose your travel dates.
- **Budget**: Set your budget in INR.

Click the **Generate Itinerary** button, and the system will provide personalized suggestions for flights, hotels, weather, and events based on the details you entered.

## Example

### Input:

- **Destination**: Paris
- **Trip Duration**: 7 days
- **Departure Date**: 2025-06-01
- **Return Date**: 2025-06-08
- **Budget**: ₹150,000

### Output:

- **Flights**: Live flight data with details such as altitude, velocity, and estimated round-trip cost.
- **Hotel**: Hotel options within the budget.
- **Weather**: Current weather for the destination.
- **Events**: Events happening during the trip.

## How It Works

1. **LangGraph** is used for agent orchestration, which manages interactions between different tools (flight search, hotel search, weather, event suggestions).
2. **OpenSky API** provides live flight data based on the destination and coordinates.
3. **OpenStreetMap (Nominatim)** is used for geocoding to find the coordinates of the destination.
4. **Cohere** is used to generate natural language responses and conversational AI capabilities.
5. **Streamlit** offers a simple interface for users to input their travel details and receive the generated itinerary.

