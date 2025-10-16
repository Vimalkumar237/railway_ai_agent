import streamlit as st
import requests
from datetime import datetime
from service.voice_agent import call_summary_with_voice

# --- Helper Functions (moved to top) ---
def get_user_location():
    """Get user's approximate location"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data.get('city', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'lat': data.get('lat', 0),
                'lon': data.get('lon', 0)
            }
    except:
        pass
    return {'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown', 'lat': 0, 'lon': 0}


def call_mcp_search_trains(from_station, to_station, date):
    """Call the Indian Railway search trains MCP function (demo data)"""
    demo_results = f"""
🚆 TRAINS FROM {from_station} TO {to_station} ({date})

Train    Name                Departure      Arrival        Duration  Classes  Days
---------------------------------------------------------------------------------
12617   MANGALA EXPRESS      {from_station} 15:20 → {to_station} 20:02 04:42H   1A,2A,3A,SL SMTWTFS
12243   SHATABDI EXP         {from_station} 07:15 → {to_station} 11:18 04:03H   EC,CC    SMWTFS
22639   ALLEPPEY EXP         {from_station} 20:55 → {to_station} 01:22 04:27H   1A,2A,3A,SL SMTWTFS
12675   KOVAI EXPRESS        {from_station} 06:10 → {to_station} 11:02 04:52H   CC,2S    SMTWTFS

💡 Note: This is demo data. For real-time information, API integration is needed.
"""
    return demo_results


def call_mcp_live_status(train_no, date):
    """Call the Indian Railway live status MCP function (demo data)"""
    demo_status = f"""
🚆 LIVE STATUS: {train_no} ({date})

Current Status: RUNNING ON TIME
Last Updated: {datetime.now().strftime('%H:%M')}

Station Wise Status:
--------------------
📍 Chennai Central (MAS)    - Departed: 15:20 (On Time)
📍 Katpadi Junction (KPD)   - Departed: 16:45 (5 min delay)
📍 Bangalore City (SBC)     - Expected: 19:30 (10 min delay)
📍 Salem Junction (SA)      - Expected: 20:12 (10 min delay)

Next Station: Bangalore City (SBC) - ETA: 19:30

💡 Note: This is demo data. For real-time tracking, API integration is needed.
"""
    return demo_status


# --- Streamlit UI Setup ---
st.set_page_config(page_title="Indian Train Assistant", page_icon="🚆", layout="wide")
st.title("🚆 Indian Train Tracker + Voice Assistant")

# --- Sidebar: User Location & Voice API Config ---
st.sidebar.header("📍 Your Location")
with st.sidebar:
    if st.button("🔍 Detect Location"):
        location = get_user_location()
        if location['city'] != 'Unknown':
            st.success(f"📍 {location['city']}, {location['region']}")
            st.info(f"🌍 {location['country']}")
            # Find nearby stations based on location
            if location['country'].lower() == 'india':
                if 'chennai' in location['city'].lower() or 'madras' in location['city'].lower():
                    st.write("🚆 **Nearby Stations:** MAS (Chennai Central), MSB (Chennai Beach)")
                elif 'delhi' in location['city'].lower():
                    st.write("🚆 **Nearby Stations:** NDLS (New Delhi), DLI (Delhi)")
                elif 'mumbai' in location['city'].lower() or 'bombay' in location['city'].lower():
                    st.write("🚆 **Nearby Stations:** CST (Mumbai CST), BCT (Mumbai Central)")
                elif 'bangalore' in location['city'].lower() or 'bengaluru' in location['city'].lower():
                    st.write("🚆 **Nearby Stations:** SBC (Bangalore City), YPR (Yesvantpur)")
                elif 'hyderabad' in location['city'].lower():
                    st.write("🚆 **Nearby Stations:** HYB (Hyderabad), SC (Secunderabad)")
                else:
                    st.write("🚆 Use station codes for your city")
        else:
            st.warning("Could not detect location")

st.sidebar.header("📞 Voice API Configuration")
receiver_number = st.sidebar.text_input("Receiver Phone Number")

st.sidebar.header("📧 Email Configuration")
user_email = st.sidebar.text_input("Your Email Address", placeholder="your.email@gmail.com", help="Enter your Gmail address to receive train information and call details")

# Email notification toggle
send_email_notifications = st.sidebar.checkbox("📧 Send email notifications", value=True, help="Receive detailed information via email")

# --- Tab Layout ---
tab1, tab2, tab3 = st.tabs(["🚆 Train Search", "📊 Live Status", "🤖 Railway Voice Agent"])

# --- Tab 1: Train Search ---
with tab1:
    st.subheader("🔍 Search Trains Between Stations")
    
    col1, col2 = st.columns(2)
    with col1:
        from_station = st.text_input("From Station Code (e.g., MAS, NDLS, SBC)")
    with col2:
        to_station = st.text_input("To Station Code (e.g., SA, BCT, ERS)")
    
    travel_date = st.date_input("Travel Date", value=datetime.today(), key="search_travel_date")
    
    sms_enabled = st.checkbox("📲 Also send results via SMS", value=False, help="Sends a summary SMS to your phone number from the sidebar")
    if st.button("Search Trains", type="primary"):
        if not from_station or not to_station:
            st.warning("Please enter both origin and destination station codes.")
        else:
            with st.spinner("Searching for trains..."):
                try:
                    # Format date for the API
                    date_str = travel_date.strftime("%Y%m%d")
                    
                    # Call the MCP search function
                    result = call_mcp_search_trains(
                        from_station=from_station.upper(),
                        to_station=to_station.upper(),
                        date=date_str
                    )
                    
                    st.success("Search completed!")
                    st.text(result)
                    
                                                                # Send email if configured
                    if send_email_notifications and user_email:
                        try:
                            from service.simple_file_email_service import send_railway_email_file as send_railway_email
                            
                            train_data = {
                                'search_results': result,
                                'from_station': from_station.upper(),
                                'to_station': to_station.upper(),
                                'date': date_str
                            }
                            
                            with st.spinner("📧 Saving email with train information..."):
                                email_result = send_railway_email(user_email, train_data=train_data)
                            
                            if email_result.get("status") == "success":
                                st.success("📧 Email saved successfully!")
                                st.info(f"📁 Saved to: {email_result.get('filepath', 'emails/')}")
                            else:
                                st.warning(f"📧 Email not saved: {email_result.get('message')}")
                                
                        except Exception as email_error:
                            st.warning(f"📧 Email error: {email_error}")

                    # Send SMS if enabled and phone provided
                    if sms_enabled and receiver_number:
                        try:
                            from service.twilio_service import send_sms
                            sms_text = f"Trains {from_station.upper()}→{to_station.upper()} on {date_str}:\n" + "\n".join([l for l in result.splitlines()[4:8]])
                            sms_res = send_sms(receiver_number, sms_text[:1500])
                            if sms_res.get("status") == "success":
                                st.success("📲 SMS sent successfully!")
                            else:
                                st.warning(f"📲 SMS not sent: {sms_res.get('message')}")
                        except Exception as sms_error:
                            st.warning(f"📲 SMS error: {sms_error}")
                    
                except Exception as e:
                    st.error(f"Failed to search trains: {e}")
                    st.info("💡 Try using station codes like MAS (Chennai), NDLS (New Delhi), SBC (Bangalore)")

# --- Tab 2: Live Status ---
with tab2:
    st.subheader("📊 Check Train Live Status")
    
    train_number = st.text_input("Train Number (e.g., 12617)")
    status_date = st.date_input("Date for Status", value=datetime.today(), key="status_date")
    
    sms_enabled_ls = st.checkbox("📲 Also send live status via SMS", value=False)
    if st.button("Check Live Status", type="primary"):
        if not train_number:
            st.warning("Please enter a train number.")
        else:
            with st.spinner("Checking live status..."):
                try:
                    date_str = status_date.strftime("%Y-%m-%d")
                    result = call_mcp_live_status(train_no=train_number, date=date_str)
                    
                    st.success("Live status retrieved!")
                    st.text(result)
                    
                    # Send email if configured
                    if send_email_notifications and user_email:
                        try:
                            from service.simple_file_email_service import send_railway_email_file as send_railway_email
                            
                            train_data = {
                                'live_status': result,
                                'train_number': train_number,
                                'status_date': date_str
                            }
                            
                            with st.spinner("📧 Saving email with live status..."):
                                email_result = send_railway_email(user_email, train_data=train_data)
                            
                            if email_result.get("status") == "success":
                                st.success("📧 Email saved successfully!")
                                st.info(f"📁 Saved to: {email_result.get('filepath', 'emails/')}")
                            else:
                                st.warning(f"📧 Email not saved: {email_result.get('message')}")
                                
                        except Exception as email_error:
                            st.warning(f"📧 Email error: {email_error}")

                    if sms_enabled_ls and receiver_number:
                        try:
                            from service.twilio_service import send_sms
                            sms_text = f"Live status {train_number} ({date_str}):\n" + "\n".join(result.splitlines()[4:9])
                            sms_res = send_sms(receiver_number, sms_text[:1500])
                            if sms_res.get("status") == "success":
                                st.success("📲 SMS sent successfully!")
                            else:
                                st.warning(f"📲 SMS not sent: {sms_res.get('message')}")
                        except Exception as sms_error:
                            st.warning(f"📲 SMS error: {sms_error}")
                    
                except Exception as e:
                    st.error(f"Failed to get live status: {e}")

# --- Tab 3: Railway Voice Agent ---
with tab3:
    st.subheader("🤖 AI Railway Booking Voice Agent")
    st.info("💡 This intelligent voice agent can help you with railway bookings, train information, and travel assistance!")
    
    # Booking options
    col1, col2 = st.columns(2)
    with col1:
        booking_type = st.selectbox(
            "What would you like the agent to help with?",
            [
                "Book train tickets",
                "Check train availability", 
                "Get train schedules",
                "Check booking status",
                "Cancel/modify booking",
                "General train information"
            ]
        )
    
    with col2:
        urgency = st.selectbox("Urgency Level", ["Normal", "Urgent", "Emergency"])
    
    # Route info for booking
    if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"]:
        st.write("**Travel Details:**")
        route_col1, route_col2, route_col3 = st.columns(3)
        
        with route_col1:
            journey_from = st.text_input("From Station", placeholder="e.g., Chennai")
        with route_col2:
            journey_to = st.text_input("To Station", placeholder="e.g., Salem")
        with route_col3:
            journey_date = st.date_input("Travel Date", value=datetime.today(), key="agent_travel_date")
    
    # Generate intelligent voice message
    def generate_voice_message(booking_type, urgency, journey_from=None, journey_to=None, journey_date=None):
        base_message = f"Hello! This is your AI Railway Assistant calling with {urgency.lower()} priority. "
        
        if booking_type == "Book train tickets":
            message = base_message + f"I'm calling to help you book train tickets from {journey_from} to {journey_to} for {journey_date.strftime('%B %d, %Y') if journey_date else 'your travel date'}..."
        elif booking_type == "Check train availability":
            message = base_message + f"I'm calling to provide you with train availability information from {journey_from} to {journey_to}..."
        elif booking_type == "Get train schedules":
            message = base_message + f"I'm calling with train schedule information for your route from {journey_from} to {journey_to}..."
        elif booking_type == "Check booking status":
            message = base_message + "I'm calling to help you check your train booking status..."
        elif booking_type == "Cancel/modify booking":
            message = base_message + "I'm calling to assist you with canceling or modifying your train booking..."
        else:
            message = base_message + "I'm calling to provide you with general train information and travel assistance..."
        
        message += " I'm here to make your railway travel experience smooth and convenient. How can I assist you today?"
        return message
    
    custom_message = st.text_area("Custom Message (Optional)", placeholder="Add any specific instructions or details for the voice agent...")
    
    # Add test and interactive call buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧪 Test Voice Integration", type="secondary"):
            try:
                from service.voice_agent import test_voice_integration
                with st.spinner("Testing voice integration..."):
                    test_result = test_voice_integration()
                
                if test_result.get("status") == "initiated":
                    st.success("✅ Voice integration test successful!")
                    st.info("You should receive a test call shortly.")
                else:
                    st.error(f"❌ Test failed: {test_result.get('message')}")
                    
                with st.expander("🔧 Test Details"):
                    st.write(test_result)
            except Exception as e:
                st.error(f"Test error: {e}")
    
        with col2:
            if st.button("🚀 Call Railway Agent", type="primary"):
                if not receiver_number:
                    st.warning("Please enter your phone number in the sidebar.")
                else:
                    try:
                        if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"]:
                            if not journey_from or not journey_to:
                                st.warning("Please enter travel details (From and To stations).")
                            else:
                                ai_message = generate_voice_message(booking_type, urgency, journey_from, journey_to, journey_date)
                        else:
                            ai_message = generate_voice_message(booking_type, urgency)
                        
                        if custom_message.strip():
                            ai_message += f" Additional details: {custom_message.strip()}"
                        
                        from config import ELEVENLABS_API_KEY, TWILIO_FROM_NUMBER
                        
                        with st.spinner("Initiating AI Railway Agent call..."):
                            result = call_summary_with_voice(ELEVENLABS_API_KEY, TWILIO_FROM_NUMBER, receiver_number, ai_message)
                        
                        # Check if call was successful
                        if result.get("status") == "initiated":
                            st.success("🎉 AI Railway Agent call initiated successfully!")
                            st.info(f"**Call Type:** {booking_type}")
                            st.info(f"**Priority:** {urgency}")
                            if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"]:
                                st.info(f"**Route:** {journey_from} → {journey_to}")
                                st.info(f"**Date:** {journey_date.strftime('%B %d, %Y')}")
                            
                            with st.expander("📞 Call Details"):
                                st.write(result)
                                st.write("**Message sent:**")
                                st.write(ai_message)
                            
                            # Send email with call details
                            if send_email_notifications and user_email:
                                try:
                                    from service.simple_file_email_service import send_railway_email_file as send_railway_email
                                    
                                    call_details = {
                                        'call_type': booking_type,
                                        'priority': urgency,
                                        'call_sid': result.get('call_sid'),
                                        'status': result.get('status'),
                                        'timestamp': result.get('timestamp'),
                                        'message': ai_message,
                                        'journey_from': journey_from if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"] else None,
                                        'journey_to': journey_to if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"] else None,
                                        'journey_date': journey_date.strftime('%B %d, %Y') if booking_type in ["Book train tickets", "Check train availability", "Get train schedules"] else None
                                    }
                                    
                                    with st.spinner("📧 Saving email with call details..."):
                                        email_result = send_railway_email(user_email, call_details=call_details)
                                    
                                    if email_result.get("status") == "success":
                                        st.success("📧 Call details saved to file!")
                                        st.info(f"📁 Saved to: {email_result.get('filepath', 'emails/')}")
                                    else:
                                        st.warning(f"📧 Email not saved: {email_result.get('message')}")
                                        
                                except Exception as email_error:
                                    st.warning(f"📧 Email error: {email_error}")
                        else:
                            st.error(f"❌ Call failed: {result.get('message', 'Unknown error')}")
                            st.warning("💡 Troubleshooting tips:")
                            st.write("1. Check if your phone number is correct")
                            st.write("2. Verify API keys are configured in config.py")
                            st.write("3. Ensure you have sufficient Twilio credits")
                            st.write("4. Check if the phone number is in correct format (+country code)")
                            
                            with st.expander("🔧 Technical Details"):
                                st.write(result)
                                st.write("**Message that was supposed to be sent:**")
                                st.write(ai_message)
                            
                    except Exception as e:
                        st.error(f"Voice agent error: {e}")
                        st.info("Make sure you have configured your API keys in config.py")
    
        with col3:
            if st.button("🗣️ Interactive Call", type="primary"):
                if not receiver_number:
                    st.warning("Please enter your phone number in the sidebar.")
                else:
                    try:
                        from service.simple_interactive_agent import create_simple_interactive_call, get_interactive_features
                        from config import TWILIO_FROM_NUMBER
                        
                        with st.spinner("Initiating interactive AI call..."):
                            result = create_simple_interactive_call(receiver_number, TWILIO_FROM_NUMBER)
                        
                        if result.get("status") == "initiated":
                            st.success("🎉 Interactive AI call initiated!")
                            st.info("**This is a demonstration of interactive voice calls!**")
                            
                            features = get_interactive_features()
                            st.info("**Interactive Features:**")
                            for feature in features["features"]:
                                st.write(f"• {feature}")
                            
                            st.info("**Example questions you can ask in full implementation:**")
                            for question in features["example_questions"][:4]:
                                st.write(f"• '{question}'")
                            
                            with st.expander("📞 Interactive Call Details"):
                                st.write(result)
                                st.write("**Setup for full interactivity:**")
                                for step in features["setup_required"]:
                                    st.write(f"• {step}")
                            
                            # Send email with interactive call details
                            if send_email_notifications and user_email:
                                try:
                                    from service.simple_file_email_service import send_railway_email_file as send_railway_email
                                    
                                    call_details = {
                                        'call_type': 'Interactive Railway Call',
                                        'priority': 'Normal',
                                        'call_sid': result.get('call_sid'),
                                        'status': result.get('status'),
                                        'timestamp': result.get('timestamp'),
                                        'message': 'Interactive demonstration call explaining how two-way conversations work with the AI Railway Assistant'
                                    }
                                    
                                    with st.spinner("📧 Saving email with interactive call details..."):
                                        email_result = send_railway_email(user_email, call_details=call_details)
                                    
                                    if email_result.get("status") == "success":
                                        st.success("📧 Interactive call details saved to file!")
                                        st.info(f"📁 Saved to: {email_result.get('filepath', 'emails/')}")
                                    else:
                                        st.warning(f"📧 Email not saved: {email_result.get('message')}")
                                        
                                except Exception as email_error:
                                    st.warning(f"📧 Email error: {email_error}")
                        else:
                            st.error(f"❌ Interactive call failed: {result.get('message', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"Interactive call error: {e}")
                        st.info("Make sure you have configured your API keys in config.py")

# --- Help Section ---
with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    ### 🚆 Train Search
    - Enter station codes (e.g., MAS for Chennai, NDLS for New Delhi)
    - Select travel date
    - Click "Search Trains" to find available trains
    
    ### 📊 Live Status
    - Enter train number (e.g., 12617)
    - Select date to check status
    - Click "Check Live Status" to see current train location
    
    ### 🤖 Railway Voice Agent
    - Enter your phone number in the sidebar
    - Select what you need help with (booking, availability, etc.)
    - Choose urgency level and enter travel details
    - Click "Call Railway Agent" to receive an intelligent AI call
    - The agent will provide personalized railway assistance
    
    ### 📧 Email Notifications
    - Enter your Gmail address in the sidebar
    - Enable email notifications checkbox
    - All train searches, live status, and call details will be sent to your email
    - Receive beautiful HTML emails with complete information
    
    ### Common Station Codes:
    - MAS: Chennai Central
    - NDLS: New Delhi
    - SBC: Bangalore City
    - SA: Salem
    - ERS: Ernakulam
    - BCT: Mumbai Central
    """)

# --- Demo Data Section ---
with st.expander("📋 Demo Data"):
    st.markdown("""
    ### Sample Train Numbers:
    - 12617: Mangala Lakshadweep Express
    - 12243: Shatabdi Express
    - 20643: Vande Bharat Express
    
    ### Sample Routes:
    - MAS → SA: Chennai to Salem
    - NDLS → BCT: New Delhi to Mumbai
    - SBC → ERS: Bangalore to Ernakulam
    """)
