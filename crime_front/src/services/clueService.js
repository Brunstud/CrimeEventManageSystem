import axiosInstance from './axiosInstance';

const API_URL = '/clues/';

/**
 * 获取所有线索列表
 * @returns {Promise<Object>} - 返回所有线索列表
 */
export const getAllClues = async () => {
  try {
    const response = await axiosInstance.get(API_URL);
    return response.data;
  } catch (error) {
    console.error('获取线索列表失败:', error);
    throw error;
  }
};

/**
 * 获取指定案件的线索列表
 * @param {number} eventId - 案件ID
 * @returns {Promise<Object>} - 返回该案件的线索列表
 */
export const getCluesByEventId = async (eventId) => {
  try {
    const response = await axiosInstance.get(`${API_URL}${eventId}/`);
    return response.data;
  } catch (error) {
    console.error(`获取案件ID ${eventId} 的线索失败:`, error);
    throw error;
  }
};

/**
 * 提交新的案件线索
 * @param {Object} clueData - 线索数据
 * @param {number} clueData.event_id - 案件ID
 * @param {string} clueData.clue_type - 线索类型
 * @param {string} clueData.clue_description - 线索描述
 * @param {boolean} clueData.chosen_as_evidence - 是否选为证据
 * @returns {Promise<Object>} - 返回提交结果
 */
export const uploadClue = async (clueData) => {
  try {
    const response = await axiosInstance.post(API_URL, clueData);
    return response.data;
  } catch (error) {
    console.error('提交线索失败:', error);
    throw error;
  }
};


/**
 * 搜索线索
 * @param {string} keyword - 搜索关键词
 * @param {number} [eventId] - 可选的案件ID，用于搜索特定案件的线索
 * @returns {Promise<Object>} - 返回搜索结果，包含分页信息
 */
export const searchClues = async (keyword, eventId = null) => {
  try {
    const url = eventId 
      ? `/clues/${eventId}/clues_for_event/?search=${keyword}`
      : `/clues/?search=${keyword}`;
    const response = await axiosInstance.get(url);
    return response.data;
  } catch (error) {
    console.error('搜索线索失败:', error);
    throw error;
  }
};
