import API from "./api";

const BASE = "/api/admin";

export const adminDashboard = async () => {
  try {
    const response = await API.get(`${BASE}`);
    return response.data;
  } catch (error) {
    throw new Error("Unable to get the admin analytics");
  }
};

export const dashboardTrends = async () => {
  try {
    const response = await API.get(`${BASE}/appointments-trend`);
    return response.data;
  } catch (error) {
    throw new Error("Unable to fetch the analytics graph");
  }
};

export const getDoctors = async (page) => {
  try {
    const response = await API.get(`${BASE}/doctors?page=${page}`);
    return response.data;
  } catch (error) {
    throw new Error("Unable to get the doctors data");
  }
};

export const getDoctorList = async() => {
    try {
    const response = await API.get(`${BASE}/doctors_name`);
    return response.data;
  } catch (error) {
    throw new Error("Unable to get the doctors data");
  }
}

export const filterDoctors = async (params) => {
  try {
    const response = await API.get(`/api/admin/doctors-filter`,{
      params
    })
    return response.data
  } catch (error) {
    throw new Error("Unable to filter doctors")
  }
}

export const updateDoc = async (id, formData) => {
  try {
    const response = await API.put(`${BASE}/doctors/${id}`, formData);
    return response.data;
  } catch (error) {
    throw new Error("Unable to update the doctor's data");
  }
};

export const updateDocStatus = async (id, stat) => {
  try {
    const response = await API.put(`${BASE}/doctors/${id}/status`, {
      status: stat,
    });
    return response.data;
  } catch (error) {
    throw new Error("Unable to update the status");
  }
};

export const addDoctor = async (formData) => {
  try {
    const response = await API.post(`${BASE}/add-doctor`, formData);
    return response.data;
  } catch (error) {
    throw new Error("Unable to add doctor");
  }
};

export const getPatients = async (params) => {
  try {
    const response = await API.get(`${BASE}/patients`,{
      params
    })
    return response.data;
  } catch (error) {
    throw new Error("Unable to fetch the patient lists")
  }
}

export const getAppointment = async (params) => {
  try {
    const response = await API.get(`${BASE}/appointments`,{
      params
    })
    return response.data
  } catch (error) {
    throw new Error("Unable to fetcht the appointments");
  }
}
