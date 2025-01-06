import axiosInstance from './axiosInstance';

const API_URL = '/residents/';

/**
 * 获取所有居民列表
 * @returns {Promise<Object>} - 返回居民列表数据，包含总数和居民信息数组
 */
export const getAllResidents = async () => {
  try {
    const response = await axiosInstance.get(API_URL);
    return response.data;
  } catch (error) {
    console.error('获取居民列表失败:', error);
    throw error;
  }
};

/**
 * 获取指定居民的详细信息
 * @param {string|number} residentId - 居民ID
 * @returns {Promise<Object>} - 返回居民的详细信息
 */
export const getResidentDetail = async (residentId) => {
  try {
    const response = await axiosInstance.get(`${API_URL}${residentId}/`);
    return response.data;
  } catch (error) {
    console.error('获取居民详细信息失败:', error);
    throw error;
  }
};


/**
 * 搜索居民信息
 * @param {string} keyword - 搜索关键词
 * @returns {Promise<Object>} - 返回搜索结果，包含分页信息
 */
export const searchResidents = async (keyword) => {
    try {
      const response = await axiosInstance.get(`${API_URL}/?search=${keyword}`);
      return response.data;
    } catch (error) {
      console.error('搜索居民信息失败:', error);
      throw error;
    }
  };
  