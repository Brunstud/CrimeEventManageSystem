<template>
  <div class="register">
    <div class="register-container">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>姓名</label>
          <input 
            v-model="fullname" 
            placeholder="请输入您的姓名"
            class="form-input"
            required 
          />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="请输入您的邮箱"
            class="form-input"
            required 
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="请输入密码"
            class="form-input"
            required 
          />
        </div>
        <div class="form-group">
          <label>联系方式</label>
          <input 
            v-model="contact" 
            placeholder="请输入您的联系方式"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>地址</label>
          <input 
            v-model="address" 
            placeholder="请输入您的地址"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>角色</label>
          <select v-model="selectedRole" class="form-input" @change="updateRole">
            <option value="Visitor">访客</option>
            <option value="Related">相关人员</option>
            <option value="Officer">警官</option>
            <option value="Cid">刑事侦查员</option>
            <option value="Admin">管理员</option>
          </select>
        </div>
        <button type="submit" class="submit-btn">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
import { register } from '@/services/authService';
import { Message } from 'element-ui';

export default {
  name: 'UserRegistration',
  data() {
    return {
      fullname: '',
      email: '',
      password: '',
      contact: '',
      address: '',
      selectedRole: 'Visitor',
      roleMapping: {
        'Visitor': 'Visitor',
        'Related': 'Related',
        'Officer': 'Officer',
        'Cid': 'Cid',
        'Admin': 'Admin'
      }
    };
  },
  methods: {
    updateRole() {
      // 根据选择的角色更新实际的role值
      return this.roleMapping[this.selectedRole];
    },
    /**
     * 处理用户注册
     */
    async handleRegister() {
      try {
        const role = this.updateRole();
        console.log("Try register:", this.fullname, this.email, this.password, this.contact, this.address, role);
        await register(this.fullname, this.email, this.password, this.contact, this.address, role);
        Message.success("注册成功!");
        this.$router.push('/login'); // 注册成功后跳转到登录页面
      } catch (error) {
        console.error("Registration failed:", error); // 打印错误信息
        // 显示错误提示
        Message.error("注册失败,请检查您的信息后重试。");
      }
    }
  }
};
</script>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-container {
  background: white;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5em;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.2em;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}

.form-group label {
  color: #666;
  font-size: 0.9em;
}

.form-input {
  padding: 0.8em;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #409EFF;
}

.submit-btn {
  background-color: #409EFF;
  color: white;
  padding: 0.8em;
  border: none;
  border-radius: 4px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #66b1ff;
}
</style>