import API from './api';

const BASE_URL = '/api/patients';

export const getDashDetails = async() => {
    try {
        const response = await API.get(`${BASE_URL}/dashboard`);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getDoctors = async(params) => {
    try {
        const response = await API.get(`${BASE_URL}/doctors`, { params });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getDocDetails = async(id) => {
    try {
        const response = await API.get(`${BASE_URL}/doctors/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const bookAppointment = async(data) => {
    try {
        const response = await API.post(`/api/appointments`, data);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const rescheduleAppointment = async(id, data) => {
    try {
        const response = await API.patch(`/api/patients/appointments/${id}/reschedule`, data);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const cancelAppointment = async(id) => {
    try {
        const response = await API.delete(`/api/patients/appointments/${id}/cancel`);
        return response.data;
    }catch(error){
        throw error;
    }
}

export const myAppointments = async(params) => {
    try {
        const response = await API.get(`${BASE_URL}/my-appointments`, { params });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getAppointmentDetails = async(id) => {
    try {
        const response = await API.get(`${BASE_URL}/appointments/${id}`);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const medHistory = async() => {
    try {
        const response = await API.get(`${BASE_URL}/medical-history`);
        return response.data;
    } catch (error) {
        throw error;
    }
}