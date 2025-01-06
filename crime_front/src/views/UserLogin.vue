<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">用户登录</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">账号</label>
          <input 
            id="email"
            v-model="email" 
            type="text"
            placeholder="请输入账号/邮箱"
            :class="{'error': errors.email}"
          />
          <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input 
            id="password"
            v-model="password" 
            type="password"
            placeholder="请输入密码"
            :class="{'error': errors.password}"
          />
          <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
        </div>

        <button type="submit" class="login-btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        
        <button type="button" class="register-btn" @click="goToRegister">
          注册账号
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/authService';
import { Message } from 'element-ui';

export default {
  name: 'UserLogin',
  data() {
    return {
      email: '',
      password: '',
      errors: {
        email: '',
        password: ''
      },
      isLoading: false
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        email: '',
        password: ''
      };

      if (!this.email.trim()) {
        this.errors.email = '请输入账号';
        isValid = false;
      }

      if (!this.password) {
        this.errors.password = '请输入密码';
        isValid = false;
      } else if (this.password.length < 6) {
        this.errors.password = '密码长度不能小于6位';
        isValid = false;
      }

      return isValid;
    },
    async handleLogin() {
      if (!this.validateForm()) return;
      
      this.isLoading = true;
      try {
        await login(this.email, this.password);
        Message.success("登录成功!");
        if (this.$route.path !== "/") {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("登录失败:", error);
        Message.error("登录失败,请检查账号密码是否正确");
      } finally {
        this.isLoading = false;
      }
    },
    goToRegister() {
      this.$router.push('/register');
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.login-box {
  width: 420px;
  padding: 2.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.login-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2.5rem;
  font-size: 2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  color: #4a5568;
  font-size: 1rem;
  font-weight: 500;
}

input {
  padding: 1rem 1.2rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

input:focus {
  outline: none;
  border-color: #4299e1;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
}

input.error {
  border-color: #e53e3e;
  background-color: #fff5f5;
}

.error-message {
  color: #e53e3e;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 0.2rem;
}

.login-btn {
  background-color: #3182ce;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.login-btn:hover {
  background-color: #2b6cb0;
  transform: translateY(-1px);
}

.login-btn:disabled {
  background-color: #90cdf4;
  cursor: not-allowed;
  transform: none;
}

.register-btn {
  background-color: #48bb78;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.register-btn:hover {
  background-color: #38a169;
  transform: translateY(-1px);
}
</style>