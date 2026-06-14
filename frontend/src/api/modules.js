import { api } from "./client";

export const lockersApi = {
  list: () => api.get("/lockers/cells/"),
  summary: () => api.get("/lockers/cells/summary/"),
  reset: (id) => api.post(`/lockers/cells/${id}/reset/`, {}),
  markMaintenance: (id) => api.post(`/lockers/cells/${id}/mark_maintenance/`, {}),
};

export const parcelsApi = {
  list: () => api.get("/parcels/"),
  inbound: (payload) => api.post("/parcels/inbound/", payload),
  open: (pickupCode, operator) => api.post("/parcels/open/", { pickup_code: pickupCode, operator }),
  reportException: (payload) => api.post("/parcels/report_exception/", payload),
};

export const notificationsApi = {
  list: () => api.get("/notifications/"),
};

export const returnsApi = {
  list: () => api.get("/returns/"),
  create: (payload) => api.post("/returns/", payload),
  complete: (id) => api.post(`/returns/${id}/complete/`, {}),
};

export const handoversApi = {
  listShifts: () => api.get("/handovers/shifts/"),
  createShift: (payload) => api.post("/handovers/shifts/", payload),
  getStats: (params) => api.get("/handovers/shifts/stats/", { params }),
  listExceptions: () => api.get("/handovers/exceptions/"),
};
