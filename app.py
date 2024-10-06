from flask import Flask, jsonify
import os

from supabase import create_client, Client


app = Flask(__name__)

supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)


@app.route('/events', methods=['GET'])
def get_events():
    """
    Retrieve a list of all events.
    """
    try:
        response = supabase.table('events').select('*').execute()
        events = response.data
        return jsonify({'events': events}), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Error fetching events'}), 500

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
    Retrieve details of a specific event by ID.
    """
    try:
        response = supabase.table('events').select('*').eq('id', event_id).execute()
        event_data = response.data
        if not event_data:
            return jsonify({"error": "Event not found"}), 404
        event = event_data[0]
        return jsonify({'event': event}), 200
    except Exception as e:
        print(f"Error fetching event: {e}")
        return jsonify({'error': 'Error fetching event'}), 500

@app.route('/events/<int:event_id>/companies', methods=['GET'])
def get_companies_for_event(event_id):
    """
    Retrieve companies that match a specific event.
    """
    # Fetch event details
    try:
        response = supabase.table('events').select('*').eq('id', event_id).execute()
        event_data = response.data
        if not event_data:
            return jsonify({"error": "Event not found"}), 404
        event = event_data[0]
    except Exception as e:
        print(f"Error fetching event: {e}")
        return jsonify({"error": "Error fetching event"}), 500

    # Fetch matching companies
    try:
        response = supabase.rpc('get_event_companies', {'event_id_input': event_id}).execute()
        matching_companies = response.data
        return jsonify({
            'event': event,
            'matching_companies': matching_companies
        }), 200
    except Exception as e:
        print(f"Error fetching matching companies: {e}")
        return jsonify({"error": "Error fetching matching companies"}), 500

@app.route('/companies', methods=['GET'])
def get_companies():
    """
    Retrieve a list of all companies.
    """
    try:
        response = supabase.table('companies').select('*').execute()
        companies = response.data
        return jsonify({'companies': companies}), 200
    except Exception as e:
        print(f"Error fetching companies: {e}")
        return jsonify({'error': 'Error fetching companies'}), 500

@app.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """
    Retrieve details of a specific company by ID.
    """
    try:
        response = supabase.table('companies').select('*').eq('id', company_id).execute()
        company_data = response.data
        if not company_data:
            return jsonify({"error": "Company not found"}), 404
        company = company_data[0]
        return jsonify({'company': company}), 200
    except Exception as e:
        print(f"Error fetching company: {e}")
        return jsonify({'error': 'Error fetching company'}), 500

@app.route('/companies/<int:company_id>/events', methods=['GET'])
def get_events_for_company(company_id):
    """
    Retrieve events that match a specific company.
    """
    # Fetch company details
    try:
        response = supabase.table('companies').select('*').eq('id', company_id).execute()
        company_data = response.data
        if not company_data:
            return jsonify({"error": "Company not found"}), 404
        company = company_data[0]
    except Exception as e:
        print(f"Error fetching company: {e}")
        return jsonify({"error": "Error fetching company"}), 500

    # Fetch matching events
    try:
        response = supabase.rpc('get_company_events', {'company_id_input': company_id}).execute()
        matching_events = response.data
        return jsonify({
            'company': company,
            'matching_events': matching_events
        }), 200
    except Exception as e:
        print(f"Error fetching matching events: {e}")
        return jsonify({"error": "Error fetching matching events"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run( port=port)