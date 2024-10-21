import axios from "axios";

const api = axios.create({
  baseURL: "https://tp4yevt607.execute-api.us-east-1.amazonaws.com/Prod",
});

export default api;
