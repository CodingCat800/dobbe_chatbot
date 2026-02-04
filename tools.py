
from langchain.tools import tool
from datetime import datetime, time,date,timedelta
from external.calendar import create_calendar_event
from external.gmail import send_email_gmail_api
from sql import get_connection

def parse_date(date_text: str):
    #converts text like today tomorrow to YYYY:MM:DD format
    today = date.today()

    if date_text.lower() == "today":
        return today
    if date_text.lower() == "tomorrow":
        return today + timedelta(days=1)

    return date_text

def parse_time(time_text: str) -> time:
    #Converts '12 PM', '15:00', '2pm' to datetime format
    formats = [
        "%I %p",      # 3 PM
        "%I:%M %p",   # 3:00 PM
        "%H:%M",      # 15:00
        "%H",         # 15
    ]

    for fmt in formats:
        try:
            return datetime.strptime(time_text, fmt).time()
        except ValueError:
            continue

    raise ValueError(f"Unrecognized time format: {time_text}")

@tool
def show_doctor_availability(doctor:str, date_text:str):
    """
    Retrieve all available appointment time slots for a given doctor
    on a specified date.
    

    IMPORTANT:
    - If the doctor name or date is missing from the user query,
      the assistant should ask the user to provide the missing information and ONLY the missing information
      before calling this tool.

    Args:
        doctor: The name of the doctor should be formatted according to examples : Dr Ahuja, Dr Prashant capitalise names only alphabets 
        date_text: Date for which available slots are requested
                   (e.g. "today", "tomorrow", or "YYYY-MM-DD").

    Returns:
        A human-readable list of available time slots.
        If no slots are available, returns an appropriate message.
    """
    sql_date = parse_date(date_text)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT a.time
        FROM availability a
        JOIN doctors d ON d.id = a.doctor_id
        WHERE d.name = %s
          AND a.date = %s
          AND a.is_booked = false
        ORDER BY a.time
        """,
        (doctor, sql_date),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return f"No available slots found for {doctor} on {sql_date}."
    times = [
        t[0].strftime("%I:%M %p").lstrip("0")
        for t in rows
    ]

    return (
        f"Available slots for {doctor} on {sql_date}: "
        + ", ".join(times)
    )

'''
@tool
def check_doctor_availability(doctor: str, date_text: str, time_text: str) -> str:
    """
   Check whether a doctor has an available appointment slot
   at a given date and time.
   run only if time specified if not run show doctor availability
   IMPORTANT:
   - If the user has not specified the doctor name, date, or time,
     DO NOT call this tool.
   - Instead, ask the user to provide the missing information
     in a follow-up question.

   Args:
       doctor: Full name of the doctor.
       date_text: Date of the appointment (e.g. "today", "tomorrow", or "YYYY-MM-DD").
       time_text: Time of the appointment (e.g. "3 PM", "10 AM").

   Returns:
       A string indicating whether the slot is AVAILABLE,
       NOT AVAILABLE, or if no slot exists.
  """
    sql_date = parse_date(date_text)
    sql_time = parse_time(time_text)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.is_booked
        FROM availability a
        JOIN doctors d ON d.id = a.doctor_id
        WHERE d.name = %s
          AND a.date = %s
          AND a.time = %s
        LIMIT 1
    """, (doctor, sql_date, sql_time))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return "No slot found"

    return "AVAILABLE" if row[0] is False else "NOT AVAILABLE""
'''


@tool
def book_appointment(doctor: str, date_text: str, time_text: str, patient: str,mail_id:str):
    """
   Book an appointment for a patient with a doctor
   at a given date and time.
   Important:
      !!!! if any of the arguments are not provided by the user prompt them for those arguments and only those arguments nothing else

   Args:
       doctor: name of doctor as provided eg: Dr Ahuja capitalise or add Dr if needed
       date_text: Date of the appointment (e.g. "today", "tomorrow", or "YYYY-MM-DD").
       time_text: Time of the appointment (e.g. "3 PM", "10 AM").
       patient: Name of the patient booking the appointment.
       mail_id: mail id of the patient for sending confirmation email

   Returns:
       A confirmation message if the appointment is booked successfully.
   """
    print("doingggggggg")
    sql_date = parse_date(date_text)
    sql_time = parse_time(time_text)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
       UPDATE availability
       SET is_booked = true
       WHERE id = (
           SELECT a.id
           FROM availability a
           JOIN doctors d ON d.id = a.doctor_id
           WHERE d.name = %s
             AND a.date = %s
             AND a.time = %s
           LIMIT 1
       )
   """, (doctor, sql_date, sql_time))

    cur.execute("""
       INSERT INTO appointments (doctor_id, patient_name, date, time)
       VALUES (
           (SELECT id FROM doctors WHERE name = %s),
           %s, %s, %s
       )
   """, (doctor, patient, sql_date, sql_time))

    conn.commit()
    cur.close()
    conn.close()
    start_dt = datetime.combine(sql_date, sql_time)
    end_dt = start_dt + timedelta(minutes=30)

    event_link = create_calendar_event(
    summary=f"Appointment with {doctor}",
    description=f"Patient: {patient}",
    start_dt=start_dt,
    end_dt=end_dt,
)
    send_email_gmail_api(
    to_email=mail_id,
    subject="Doctor Appointment Confirmation",
    body=f"""
Hello {patient},

Your appointment is confirmed.

Doctor: {doctor}
Date: {sql_date}
Time: {sql_time.strftime("%I:%M %p").lstrip("0")}

Calendar Event:
{event_link}
"""
)

    return f"Appointment booked successfully Calendar event created: {event_link} and email sent"


'''@tool
def get_doctor_stats(date: str) -> str:
    """
    Retrieve summary statistics for doctor appointments
    on a given date.

    Args:
        date_text: Date for which statistics are requested
                   (e.g. "today", "yesterday", or "YYYY-MM-DD").

    Returns:
        A human-readable summary of total patient visits
        on the specified date.
    """
    
    return f"Total patients on {date}: 12, Fever cases: 4"'''



