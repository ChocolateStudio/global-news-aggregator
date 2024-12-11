// frontend/src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const newsService = {
  async aggregateNews() {
    try {
      const response = await axios.get(`${API_BASE_URL}/news/aggregate`);
      return response.data;
    } catch (error) {
      console.error('Error fetching news:', error);
      throw error;
    }
  }
};
