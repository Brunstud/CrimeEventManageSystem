<template>
    <div class="clue-upload">
      <h2>提交案件线索</h2>
      <form @submit.prevent="submitClue">
        <div class="form-group">
          <label>线索类型:</label>
          <select v-model="clueType" required>
            <option value="Weapon">武器</option>
            <option value="Witness">目击证人</option>
            <option value="Physical">物证</option>
            <option value="Other">其他</option>
          </select>
        </div>
        <div class="form-group">
          <label>线索描述:</label>
          <textarea v-model="description" placeholder="请详细描述线索信息" required></textarea>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="chosenAsEvidence">
            作为证据
          </label>
        </div>
        <div class="button-group">
          <button type="submit">提交线索</button>
          <button type="button" class="cancel-btn" @click="goBack">返回</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { uploadClue } from '@/services/clueService';
  import { Message } from 'element-ui';
  
  export default {
    name: 'ClueUpload',
    data() {
      return {
        description: '',
        clueType: 'Weapon',
        chosenAsEvidence: false
      };
    },
    methods: {
      /**
       * 提交线索
       */
      async submitClue() {
        const eventId = this.$route.params.eventId;
        const clueData = {
          event_id: eventId,
          clue_type: this.clueType,
          clue_description: this.description,
          chosen_as_evidence: this.chosenAsEvidence
        };
        try {
          console.log(clueData);
          const response = await uploadClue(clueData);
          Message.success(`线索提交成功! 线索编号: ${response.clue_code}`);
          // 跳转案件详情页
          this.$router.push(`/events/${eventId}`);
        } catch (error) {
          console.error("提交线索失败:", error);
          Message.error("提交线索失败，请重试");
        }
      },
      /**
       * 返回上一页
       */
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  .clue-upload {
    padding: 1em;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5em;
  }
  
  select, textarea {
    width: 100%;
    padding: 0.5em;
    margin-bottom: 1em;
  }
  
  textarea {
    height: 100px;
  }
  
  .button-group {
    display: flex;
    gap: 1em;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 0.5em 1em;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }

  .cancel-btn {
    background-color: #909399;
  }

  .cancel-btn:hover {
    background-color: #82848a;
  }
  </style>