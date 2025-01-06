<template>
  <div class="crime-event-form">
    <h2 class="form-title">提交犯罪事件</h2>
    <form @submit.prevent="submitCrimeEvent" class="form-container">
      <div class="form-group">
        <label for="crimeDesc" class="form-label">案情描述:</label>
        <textarea 
          v-model="crimeDesc" 
          placeholder="请输入案情描述" 
          required
          class="form-textarea"
        ></textarea>
      </div>

      <div class="form-group">
        <label class="form-label">犯罪类型:</label>
        <div class="type-selection">
          <el-select
            v-model="selectedTypes"
            multiple
            filterable
            remote
            placeholder="请选择或输入犯罪类型"
            :remote-method="searchCrimeTypes"
            :loading="loading"
            class="type-select"
          >
            <el-option
              v-for="type in crimeTypes"
              :key="type.code"
              :label="type.name"
              :value="type.code"
            >
            </el-option>
          </el-select>
          <el-button type="text" @click="showAddTypeDialog = true" class="add-type-btn">
            添加新类型
          </el-button>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">相关人员:</label>
        <div class="person-list">
          <div v-for="(person, index) in persons" :key="index" class="person-item">
            <el-select
              v-model="person.person_id"
              filterable
              remote
              placeholder="选择人员"
              :remote-method="searchPersons"
              class="person-select"
            >
              <el-option
                v-for="p in personList"
                :key="p.id"
                :label="p.name"
                :value="p.id"
              >
              </el-option>
            </el-select>
            <el-select v-model="person.relation" placeholder="选择关系" class="relation-select">
              <el-option label="嫌疑人" value="Susp"></el-option>
              <el-option label="罪犯" value="Crim"></el-option>
              <el-option label="受害者" value="Vict"></el-option>
              <el-option label="目击证人" value="Eyew"></el-option>
              <el-option label="证人" value="Witn"></el-option>
            </el-select>
            <el-button type="danger" @click="removePerson(index)" class="remove-btn">删除</el-button>
          </div>
        </div>
        <el-button type="primary" @click="addPerson" class="add-btn">添加相关人员</el-button>
      </div>

      <div class="form-group">
        <label class="form-label">武器信息:</label>
        <div class="weapon-list">
          <div v-for="(weapon, index) in weapons" :key="index" class="weapon-item">
            <el-select
              v-model="weapon.weapon_code"
              filterable
              remote
              placeholder="选择或输入武器类型"
              :remote-method="searchWeapons"
              class="weapon-select"
            >
              <el-option
                v-for="w in weaponTypes"
                :key="w.code"
                :label="w.description"
                :value="w.code"
              >
              </el-option>
            </el-select>
            <el-input
              v-model="weapon.weapon_detail"
              placeholder="武器详细描述"
              class="weapon-detail"
            ></el-input>
            <el-button type="danger" @click="removeWeapon(index)" class="remove-btn">删除</el-button>
          </div>
        </div>
        <el-button type="primary" @click="addWeapon" class="add-btn">添加武器</el-button>
      </div>

      <div class="form-group">
        <label class="form-label">区块信息:</label>
        <el-select v-model="block" placeholder="请选择区块" required class="block-select">
          <el-option
            v-for="b in blocks"
            :key="b.name"
            :label="b.description"
            :value="b.name"
          >
          </el-option>
        </el-select>
      </div>

      <div class="form-group">
        <label class="form-label">发生时间:</label>
        <el-date-picker
          v-model="timeOccurred"
          type="datetime"
          placeholder="选择日期时间"
          required
          class="date-picker"
        >
        </el-date-picker>
      </div>

      <div class="form-group">
        <label class="form-label">位置信息:</label>
        <el-input v-model="location" placeholder="位置描述" required class="location-input"></el-input>
        <div class="coordinates">
          <el-input-number
            v-model="latitude"
            :precision="6"
            placeholder="纬度"
            class="coordinate-input"
          ></el-input-number>
          <el-input-number
            v-model="longitude"
            :precision="6"
            placeholder="经度"
            class="coordinate-input"
          ></el-input-number>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">案件状态:</label>
        <el-select v-model="currentStatus" required class="status-select">
          <el-option label="已报案" value="Reported"></el-option>
          <el-option label="调查中" value="Under Investigation"></el-option>
          <el-option label="已结案" value="Closed"></el-option>
        </el-select>
      </div>

      <div class="form-actions">
        <el-button type="primary" native-type="submit" class="submit-btn">提交案件</el-button>
        <el-button type="info" @click="$router.push('/clues/upload')" class="clue-btn">提交线索</el-button>
      </div>
    </form>

    <!-- 添加新类型对话框 -->
    <el-dialog title="添加新犯罪类型" :visible.sync="showAddTypeDialog" custom-class="type-dialog">
      <el-form :model="newType" class="type-form">
        <el-form-item label="类型名称">
          <el-input v-model="newType.name"></el-input>
        </el-form-item>
        <el-form-item label="类型描述">
          <el-input v-model="newType.description"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showAddTypeDialog = false">取消</el-button>
        <el-button type="primary" @click="addNewType">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { createCrimeEvent } from '@/services/crimeEventService';
import { Message } from 'element-ui';
import { searchCrimeTypes, searchPersons, searchWeapons, addCrimeType, searchBlocks } from '@/services/searchService';

export default {
  name: 'CrimeEventForm',
  data() {
    return {
      crimeDesc: '',
      selectedTypes: [],
      crimeTypes: [], // 存储所有犯罪类型
      persons: [],
      personList: [], // 存储所有人员
      weapons: [],
      weaponTypes: [], // 存储所有武器类型
      blocks: [],
      block: '',
      timeOccurred: '',
      location: '',
      latitude: null,
      longitude: null,
      currentStatus: 'Reported',
      loading: false,
      showAddTypeDialog: false,
      newType: {
        name: '',
        description: ''
      }
    };
  },
  methods: {
    async submitCrimeEvent() {
      // 添加数据验证
      if (!this.validateForm()) {
        return;
      }

      const crimeEventData = {
        crime_description: this.crimeDesc,
        types: this.selectedTypes.map(type => ({
          type_code: type,
          order: this.selectedTypes.indexOf(type) + 1
        })),
        persons: this.persons.filter(p => p.person_id && p.relation).map(p => ({
          person_id: p.person_id,
          relation: p.relation
        })),
        weapons: this.weapons.filter(w => w.weapon_code && w.weapon_detail).map(w => ({
          weapon_code: w.weapon_code,
          weapon_detail: w.weapon_detail
        })),
        block: this.block,
        time_occurred: this.timeOccurred,
        location: this.location,
        latitude: this.latitude || 0,
        longitude: this.longitude || 0,
        current_status: this.currentStatus
      };
      console.log(crimeEventData);

      try {
        const newEvent = await createCrimeEvent(crimeEventData);
        Message.success("犯罪事件提交成功！");
        this.$router.push(`/events/${newEvent.id}`);
      } catch (error) {
        console.error("提交犯罪事件失败:", error);
        Message.error("提交失败，请检查输入并重试");
      }
    },

    // 添加表单验证方法
    validateForm() {
      if (!this.crimeDesc.trim()) {
        Message.error("请输入案情描述");
        return false;
      }

      // 验证犯罪类型
      if (!this.selectedTypes.length) {
        Message.error("请至少选择一个犯罪类型");
        return false;
      }

      // 验证相关人员
      if (!this.persons.length) {
        Message.error("请至少添加一个相关人员");
        return false;
      }
      
      if (this.persons.some(p => !p.person_id || !p.relation)) {
        Message.error("请完整填写所有相关人员信息");
        return false;
      }

      // 验证武器信息
      if (this.weapons.length && this.weapons.some(w => !w.weapon_code || !w.weapon_detail)) {
        Message.error("请完整填写所有武器信息");
        return false;
      }

      // 验证区块
      if (!this.block) {
        Message.error("请选择区块");
        return false;
      }

      // 验证地点
      if (!this.location) {
        Message.error("请输入具体地点");
        return false;
      }

      // 验证经纬度
      if (this.latitude !== null && (this.latitude < -90 || this.latitude > 90)) {
        Message.error("纬度值必须在 -90 到 90 之间");
        return false;
      }

      if (this.longitude !== null && (this.longitude < -180 || this.longitude > 180)) {
        Message.error("经度值必须在 -180 到 180 之间");
        return false;
      }

      return true;
    },

    addPerson() {
      this.persons.push({
        person_id: '',
        relation: ''
      });
    },

    removePerson(index) {
      this.persons.splice(index, 1);
    },

    addWeapon() {
      this.weapons.push({
        weapon_code: '',
        weapon_detail: ''
      });
    },

    removeWeapon(index) {
      this.weapons.splice(index, 1);
    },

    async searchCrimeTypes(query) {
      if (query) {
        // 如果有查询词,从已加载的数据中过滤
        this.crimeTypes = this.crimeTypes.filter(type => 
          type.name.toLowerCase().includes(query.toLowerCase())
        );
      } else {
        // 如果没有查询词,显示所有数据
        await this.loadAllCrimeTypes();
      }
    },

    async searchPersons(query) {
      if (query) {
        // 从已加载的数据中过滤
        this.personList = this.personList.filter(person =>
          person.name.toLowerCase().includes(query.toLowerCase())
        );
      } else {
        // 显示所有数据
        await this.loadAllPersons();
      }
    },

    async searchWeapons(query) {
      if (query) {
        // 从已加载的数据中过滤
        this.weaponTypes = this.weaponTypes.filter(weapon =>
          weapon.description.toLowerCase().includes(query.toLowerCase())
        );
      } else {
        // 显示所有数据
        await this.loadAllWeapons();
      }
    },

    async searchBlocks(query) {
      if (query) {
        // 从已加载的数据中过滤
        this.blocks = this.blocks.filter(block =>
          block.block_name.toLowerCase().includes(query.toLowerCase())
        );
      } else {
        // 显示所有数据
        await this.loadAllBlocks();
      }
    },

    async loadAllCrimeTypes() {
      try {
        this.loading = true;
        const results = await searchCrimeTypes('');
        this.crimeTypes = results;
        console.log(this.crimeTypes);
      } catch (error) {
        Message.error("加载犯罪类型失败");
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async loadAllPersons() {
      try {
        this.loading = true;
        const results = await searchPersons('');
        this.personList = results;
        console.log(this.personList);
      } catch (error) {
        Message.error("加载人员数据失败");
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async loadAllWeapons() {
      try {
        this.loading = true;
        const results = await searchWeapons('');
        this.weaponTypes = results;
        console.log(this.weaponTypes);
      } catch (error) {
        Message.error("加载武器类型失败");
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async loadAllBlocks() {
      try {
        this.loading = true;
        const results = await searchBlocks('');
        this.blocks = results;
        console.log(this.blocks);
      } catch (error) {
        Message.error("加载区块数据失败");
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async addNewType() {
      try {
        if (!this.newType.name) {
          Message.warning("请输入类型名称");
          return;
        }
        const newTypeData = await addCrimeType(this.newType.name, this.newType.description);
        Message.success("添加新类型成功");
        this.showAddTypeDialog = false;
        
        // 将新添加的类型添加到类型列表中
        this.crimeTypes.push({
          code: newTypeData.type_code,
          name: this.newType.name,
          description: this.newType.description
        });
        
        // 自动选中新添加的类型
        this.selectedTypes.push(newTypeData.type_code);
        
        // 清空表单
        this.newType.name = '';
        this.newType.description = '';
      } catch (error) {
        Message.error("添加新类型失败");
        console.error(error);
      }
    }
  },
  async created() {
    // 页面创建时加载所有数据
    await Promise.all([
      this.loadAllCrimeTypes(),
      this.loadAllPersons(),
      this.loadAllWeapons(),
      this.loadAllBlocks()
    ]);
  }
};
</script>

<style scoped>
.crime-event-form {
  padding: 2em;
  max-width: 1000px;
  margin: 0 auto;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.form-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2em;
  font-size: 24px;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 2em;
}

.form-group {
  margin-bottom: 1.5em;
  background: #f8f9fa;
  padding: 1.5em;
  border-radius: 6px;
}

.form-label {
  display: block;
  margin-bottom: 0.8em;
  font-weight: 600;
  color: #2c3e50;
}

.form-textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  resize: vertical;
}

.type-selection,
.person-list,
.weapon-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.person-item,
.weapon-item {
  display: flex;
  gap: 1em;
  align-items: center;
  background: #fff;
  padding: 1em;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.type-select,
.person-select,
.weapon-select,
.block-select,
.status-select {
  width: 100%;
}

.coordinates {
  display: flex;
  gap: 1em;
  margin-top: 1em;
}

.coordinate-input {
  flex: 1;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 1.5em;
  margin-top: 2em;
}

.submit-btn,
.clue-btn {
  padding: 12px 30px;
  font-size: 16px;
}

.add-btn {
  margin-top: 1em;
}

.remove-btn {
  padding: 8px 15px;
}

.type-dialog {
  width: 500px;
}

.dialog-footer {
  text-align: right;
}

/* Element UI 组件样式覆盖 */
:deep(.el-select),
:deep(.el-input),
:deep(.el-input-number) {
  width: 100%;
}

:deep(.el-button) {
  border-radius: 4px;
}

:deep(.el-date-picker) {
  width: 100%;
}
</style>