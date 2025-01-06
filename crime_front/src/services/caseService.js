import axiosInstance from './axiosInstance';

const API_URL = '/case-progress/';

/**
 * 获取案件进展列表
 * @param {number} eventId - 案件ID
 * @returns {Promise<Object>} - 返回案件进展列表
 */
export const getCaseProgress = async (eventId) => {
  try {
    const response = await axiosInstance.get(`${API_URL}${eventId}/`);
    return response.data;
  } catch (error) {
    console.error(`获取案件ID ${eventId} 的进展失败:`, error);
    throw error;
  }
};

/**
 * 更新案件进展
 * @param {Object} progressData - 进展数据
 * @param {number} progressData.event_id - 案件ID
 * @param {string} progressData.status - 案件状态
 * @param {string} progressData.notes - 进展说明
 * @returns {Promise<Object>} - 返回更新结果
 */
export const updateCaseProgress = async (progressData) => {
  try {
    const response = await axiosInstance.post(API_URL, progressData);
    return response.data;
  } catch (error) {
    console.error('更新案件进展失败:', error);
    throw error;
  }
};

/**
 * 搜索案件进展
 * @param {number} eventId - 案件ID
 * @param {string} keyword - 搜索关键词
 * @returns {Promise<Object>} - 返回搜索结果，包含分页信息
 */
export const searchCaseProgress = async (eventId, keyword) => {
  try {
    const response = await axiosInstance.get(`/case-progress/${eventId}/?search=${keyword}`);
    return response.data;
  } catch (error) {
    console.error('搜索案件进展失败:', error);
    throw error;
  }
};
