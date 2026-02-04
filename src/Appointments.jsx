import { useEffect, useState } from "react";

function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  const doctorId = 1; // hardcoded for demo (Dr Ahuja)

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/appointments/${doctorId}`)
      .then((res) => res.json())
      .then((data) => {
        setAppointments(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <p style={{ textAlign: "center" }}>Loading appointments...</p>;
  }

  return (
    <div style={styles.container}>
      <h2>📋 Doctor Appointments</h2>

      {appointments.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        <ul style={styles.list}>
          {appointments.map((a, idx) => (
            <li key={idx} style={styles.item}>
              <strong>{a.patient}</strong>
              <br />
              {a.date} at {a.time}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "40px auto",
    fontFamily: "Arial, sans-serif",
  },
  list: {
    listStyle: "none",
    padding: 0,
  },
  item: {
    padding: "12px",
    border: "1px solid #ccc",
    borderRadius: "6px",
    marginBottom: "10px",
    backgroundColor: "#F9F9F9",
  },
};

export default Appointments;
