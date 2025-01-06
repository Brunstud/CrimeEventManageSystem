import axiosInstance from './axiosInstance';
const API_URL = '/search/';

// 搜索区块信息
export async function searchBlocks(query = '') {
  try {
    const response = await axiosInstance.get(`${API_URL}blocks/`, {
      params: { query }
    });
    return response.data.results.map(block => ({
      name: block.block_name,
      description: block.block_description
    }));
  } catch (error) {
    console.error('搜索区块信息失败:', error);
    throw error;
  }
}

// 搜索犯罪类型
export async function searchCrimeTypes(query = '') {
  try {
    const response = await axiosInstance.get(`${API_URL}crime-types/`, {
      params: { query }
    });
    return response.data.results.map(type => ({
      code: type.type_code,
      name: type.type_name, 
      description: type.type_description
    }));
  } catch (error) {
    console.error('搜索犯罪类型失败:', error);
    throw error;
  }
}

// 搜索人员
export async function searchPersons(query = '') {
  try {
    const response = await axiosInstance.get(`${API_URL}persons/`, {
      params: { query }
    });
    return response.data.results.map(person => ({
      id: person.person_id,
      name: person.name
    }));
  } catch (error) {
    console.error('搜索人员失败:', error);
    throw error;
  }
}

// 搜索武器类型
export async function searchWeapons(query = '') {
  try {
    const response = await axiosInstance.get(`${API_URL}weapons/`, {
      params: { query }
    });
    return response.data.results.map(weapon => ({
      code: weapon.weapon_code,
      description: weapon.weapon_description
    }));
  } catch (error) {
    console.error('搜索武器类型失败:', error);
    throw error;
  }
}

// 添加新的犯罪类型
export async function addCrimeType(typeName, description = '') {
  try {
    const response = await axiosInstance.post(`${API_URL}add-crime-type/`, {
      type_name: typeName,
      type_description: description
    });
    
    if (!response.data.success) {
      throw new Error(response.data.error);
    }
    
    return response.data.data;
  } catch (error) {
    console.error('添加犯罪类型失败:', error);
    throw error;
  }
}