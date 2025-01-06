<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>联系我们</h3>
        <p>邮箱: contact@crimesys.com</p>
        <p>电话: (555) 123-4567</p>
      </div>
      <div class="footer-section">
        <h3>快速链接</h3>
        <ul>
          <li><router-link to="/about">关于我们</router-link></li>
          <li><router-link to="/privacy">隐私政策</router-link></li>
          <li><router-link to="/terms">使用条款</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h3>关注我们</h3>
        <div class="social-links">
          <a href="#"><i class="fab fa-facebook"></i></a>
          <a href="#"><i class="fab fa-twitter"></i></a>
          <a href="#"><i class="fab fa-linkedin"></i></a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2024 Urban Crime Management System. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
.footer {
  background-color: #3b5998;
  color: white;
  padding: 2em 0;
  position: relative;
  width: 100%;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  padding: 0 20px;
}

.footer-section {
  flex: 1;
  margin: 0 15px;
}

.footer-section h3 {
  color: #ffffff;
  margin-bottom: 15px;
  font-size: 1.2em;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #ffffff;
  text-decoration: none;
  transition: opacity 0.3s;
}

.footer-section a:hover {
  opacity: 0.8;
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-links a {
  font-size: 1.5em;
}

.footer-bottom {
  text-align: center;
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-section {
    margin: 15px 0;
  }
  
  .social-links {
    justify-content: center;
  }
}
</style>