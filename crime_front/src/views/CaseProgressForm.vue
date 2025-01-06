<template>
  <div class="case-progress-form">
    <h2>更新案件进展</h2>
    <form @submit.prevent="submitProgress">
      <div class="form-group">
        <label for="status">案件状态:</label>
        <select v-model="status" required class="form-control">
          <option value="">请选择案件状态</option>
          <option value="Investigation">调查中</option>
          <option value="Arrest">已抓捕</option>
          <option value="Closed">已结案</option>
        </select>
      </div>
      <div class="form-group">
        <label for="notes">进展说明:</label>
        <textarea 
          v-model="notes" 
          placeholder="请输入案件进展详情" 
          required
          class="form-control"
          rows="4"
          maxlength="500"
        ></textarea>
        <span class="char-count">{{ notes.length }}/500</span>
      </div>
      <button type="submit" class="submit-btn" :disabled="!isFormValid">提交进展</button>
      <button type="button" class="cancel-btn" @click="goBack">取消</button>
    </form>
  </div>
</template>

<script>
import { updateCaseProgress } from '@/services/caseService';
import { Message } from 'element-ui';

export default {
  name: 'CaseProgressForm',
  data() {
    return {
      status: '',
      notes: '',
      isSubmitting: false
    };
  },
  computed: {
    isFormValid() {
      return this.status && this.notes.trim() && !this.isSubmitting;
    }
  },
  methods: {
    goBack() {
      this.$router.push(`/progress/${this.$route.params.eventId}`);
    },
    /**
     * 提交案件进展
     */
    async submitProgress() {
      if (!this.isFormValid) {
        Message.warning("请填写完整的表单信息");
        return;
      }

      this.isSubmitting = true;
      
      const progressData = {
        event_id: this.$route.params.eventId,
        status: this.status,
        notes: this.notes.trim(),
        timeProg: new Date().toISOString()
      };

      try {
        await updateCaseProgress(progressData);
        Message.success("案件进展更新成功!");
        this.$router.push(`/events/${progressData.event_id}`);
      } catch (error) {
        console.error("提交案件进展失败:", error);
        Message.error(error.response?.data?.message || "更新案件进展失败,请重试。");
      } finally {
        this.isSubmitting = false;
      }
    }
  },
  beforeRouteLeave(to, from, next) {
    if (this.notes.trim() || this.status !== '') {
      if (confirm('确定要离开吗?未保存的内容将会丢失')) {
        next();
      } else {
        next(false);
      }
    } else {
      next();
    }
  }
};
</script>

<style scoped>
.case-progress-form {
  padding: 2em;
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5em;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.5em;
  color: #606266;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.8em;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #409eff;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.char-count {
  position: absolute;
  right: 10px;
  bottom: -20px;
  font-size: 12px;
  color: #909399;
}

.submit-btn, .cancel-btn {
  width: 48%;
  padding: 0.8em;
  border: none;
  border-radius: 4px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn {
  background: #409eff;
  color: white;
  margin-right: 2%;
}

.submit-btn:hover:not(:disabled) {
  background: #66b1ff;
}

.submit-btn:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}

.cancel-btn {
  background: #f56c6c;
  color: white;
}

.cancel-btn:hover {
  background: #f78989;
}
</style>