import API from "./api";

const BASE = "/api/doctors"

export const getDoctorDashboard = async() => {
     try {
    const response = await API.get(`${BASE}/dashboard`);
    console.log("Doctor Dashboard Response:", response.data);
    return response.data;
  } catch (error) {
    console.log("Doctor Dashboard Error:", error.response);
    throw new Error("Unable to get the Doctor analytics");
  }
}

export const getPatients = async(params) => {
    try {
        const response = await API.get(`${BASE}/patients`,{
          params
        })
        return response.data
    } catch (error) {
        throw new Error("Unable to fetch the patient details")
    }
}

export const getPatientById = async(id) => {
      try {
        const response = await API.get(`${BASE}/patient-profile/${id}`)
        console.log("Patient Profile Response:", response.data);
        return response.data
    } catch (error) {
        throw new Error("Unable to fetch the patient details")
    }
}

export const getAppointments = async(params) => {
  try {
    const res = await API.get(`${BASE}/my-appointments`, { params })
    return res.data
  } catch (error) {
    throw new Error("Unable to fetch the Appointments");
  }
}

export const confirmAppointment = async(id) => {
  try {
    const res = await API.patch(`${BASE}/appointments/${id}/confirm`)
    return res.data
  } catch (error) {
    throw new Error("Unable to confirm the appointment");
  }
}

export const cancelAppointment = async(id) => {
  try {
    const res = await API.patch(`${BASE}/appointments/${id}/cancel`)
    return res.data
  } catch (error) {
    console.error("Cancel Appointment Error:", error.message);
    throw new Error("Unable to cancel the appointment");
  }
}

export const getAppointmentReport = async(id) => {
  try {
    console.log("Fetching report for appointment ID:", id);
    const res = await API.get(`${BASE}/appointments/${id}`)
    return res.data.data
  } catch (error) {
    throw new Error("Unable to fetch the appointment report");
  }
}

export const addVitals = async (id, vitalsData) => {
  try {
    const res = await API.post(
      `${BASE}/appointments/${id}/vital`,
      vitalsData
    );
    return res.data;
  } catch (error) {
    throw new Error(error?.response?.data?.error || "Unable to add vitals");
  }
};

export const addNotes = async (id, notesData) => {
  try {
    const res = await API.post(
      `${BASE}/appointments/${id}/note`,
      notesData
    );
    return res.data;
  } catch (error) {
    throw new Error(error?.response?.data?.error || "Unable to add notes");
  }
};

export const addPrescription = async (id, prescriptionData) => {
  try {
    const res = await API.post(
      `${BASE}/appointments/${id}/prescription`,
      prescriptionData
    );
    return res.data;
  } catch (error) {
    throw new Error(error?.response?.data?.error || "Unable to add prescription");
  }
};

export const addMedicalRecord = async (id, recordData) => {
  try {
    const res = await API.post(
      `${BASE}/appointments/${id}/medical-record`,
      recordData
    );
    return res.data;
  } catch (error) {
    throw new Error(error?.response?.data?.error || "Unable to add medical record");
  }
};