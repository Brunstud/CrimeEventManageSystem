import axiosInstance from './axiosInstance';

const API_URL = '/crime-events/';

/**
 * 获取所有犯罪事件列表
 * @returns {Promise<Object>} - 返回包含犯罪事件列表和总数的对象
 */
export const getAllCrimeEvents = async () => {
  try {
    const response = await axiosInstance.get(API_URL);
    return {
      count: response.data.count,
      results: response.data.results.map(event => ({
        id: event.id,
        crimeDesc: event.crime_description,
        mainType: event.main_type_name, 
        mainCriminal: event.main_criminal_name,
        mainVictim: event.main_victim_name,
        mainWeapon: event.main_weapon_name,
        timeOccurred: event.time_occurred,
        block: event.block_name,
        curStatus: event.current_status
      }))
    };
  } catch (error) {
    console.error('获取犯罪事件列表失败:', error);
    throw error;
  }
};

/**
 * 获取特定犯罪事件详情
 * @param {number} eventId - 犯罪事件ID
 * @returns {Promise<Object>} - 返回事件详细信息
 */
export const getCrimeEventById = async (eventId) => {
  try {
    const response = await axiosInstance.get(`${API_URL}${eventId}/`);
    console.log("response:", response);
    return {
      crimeDesc: response.data.crime_description,
      types: response.data.types,
      persons: response.data.persons,
      weapons: response.data.weapons,
      location: response.data.location,
      latitude: response.data.latitude,
      longitude: response.data.longitude,
      blockName: response.data.block_name,
      blockDescription: response.data.block_description,
      officers: response.data.officers,
      timeReported: response.data.time_reported,
      timeOccurred: response.data.time_occurred,
      curStatus: response.data.current_status,
      updatedAt: response.data.updated_at
    };
  } catch (error) {
    console.error(`获取犯罪事件详情失败,ID ${eventId}:`, error);
    throw error;
  }
};

/**
 * 创建新的犯罪事件
 * @param {Object} eventData - 犯罪事件数据
 * @returns {Promise<Object>} - 返回创建结果
 */
export const createCrimeEvent = async (eventData) => {
  try {
    const requestData = {
      crime_description: eventData.crime_description,
      types: eventData.types.map(type => ({
        type_code: type.type_code,
        order: type.order
      })),
      persons: eventData.persons.map(person => ({
        person_id: person.person_id,
        relation: person.relation
      })),
      weapons: eventData.weapons.map(weapon => ({
        weapon_code: weapon.weapon_code,
        weapon_detail: weapon.weapon_detail
      })),
      block: eventData.block,
      time_occurred: eventData.time_occurred,
      location: eventData.location,
      latitude: eventData.latitude,
      longitude: eventData.longitude,
      current_status: eventData.current_status
    };

    const response = await axiosInstance.post(API_URL, requestData);
    return response.data;
  } catch (error) {
    console.error("创建犯罪事件失败:", error);
    throw error;
  }
};

/**
 * 搜索犯罪事件
 * @param {string} keyword - 搜索关键词
 * @returns {Promise<Object>} - 返回搜索结果，包含分页信息
 */
export const searchCrimeEvents = async (keyword) => {
  try {
    const response = await axiosInstance.get(`${API_URL}?search=${keyword}`);
    return {
      count: response.data.count,
      results: response.data.results.map(event => ({
        id: event.id,
        crimeDesc: event.crime_description,
        mainType: event.main_type_name,
        mainCriminal: event.main_criminal_name,
        mainVictim: event.main_victim_name,
        mainWeapon: event.main_weapon_name,
        timeOccurred: event.time_occurred,
        block: event.block_name,
        curStatus: event.current_status
      }))
    };
  } catch (error) {
    console.error('搜索犯罪事件失败:', error);
    throw error;
  }
};