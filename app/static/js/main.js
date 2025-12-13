/**
 * 电子科技大学成都学院自习室预约系统 - 主要JavaScript文件
 */

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initializeTooltips();

    // 初始化表单验证
    initializeFormValidation();

    // 自动隐藏Flash消息
    autoHideFlashMessages();

    // 初始化搜索功能
    initializeSearch();
});

/**
 * 初始化Bootstrap工具提示
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 初始化表单验证
 */
function initializeFormValidation() {
    // 获取所有表单
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        // 添加提交事件监听
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        });
    });
}

/**
 * 自动隐藏Flash消息
 */
function autoHideFlashMessages() {
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');

    alerts.forEach(function(alert) {
        // 5秒后自动隐藏
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * 初始化搜索功能
 */
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;

    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        // 防抖处理，300ms后执行搜索
        searchTimeout = setTimeout(function() {
            performSearch(query);
        }, 300);
    });
}

/**
 * 执行搜索
 * @param {string} query - 搜索关键词
 */
function performSearch(query) {
    // 这里可以发送AJAX请求到后端进行搜索
    console.log('搜索关键词:', query);

    // 示例：显示加载状态
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
        if (query.length > 0) {
            resultsContainer.innerHTML = '<div class="text-center py-3"><div class="spinner-border" role="status"></div> 搜索中...</div>';
        } else {
            resultsContainer.innerHTML = '';
        }
    }
}

/**
 * 格式化日期时间
 * @param {Date|string} date - 日期对象或日期字符串
 * @param {string} format - 格式类型 ('date', 'time', 'datetime')
 * @returns {string} 格式化后的日期时间字符串
 */
function formatDateTime(date, format = 'datetime') {
    if (typeof date === 'string') {
        date = new Date(date);
    }

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    switch (format) {
        case 'date':
            return `${year}-${month}-${day}`;
        case 'time':
            return `${hours}:${minutes}`;
        case 'datetime':
        default:
            return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
}

/**
 * 确认对话框
 * @param {string} message - 确认消息
 * @param {Function} callback - 确认后的回调函数
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * 显示加载状态
 * @param {string} elementId - 元素ID
 * @param {string} message - 加载消息
 */
function showLoading(elementId, message = '加载中...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">${message}</p>
            </div>
        `;
    }
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 */
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('已复制到剪贴板', 'success');
        }).catch(function() {
            showToast('复制失败，请手动复制', 'error');
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
            showToast('已复制到剪贴板', 'success');
        } catch (err) {
            showToast('复制失败，请手动复制', 'error');
        }

        document.body.removeChild(textArea);
    }
}

/**
 * 显示Toast消息
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型 ('success', 'error', 'warning', 'info')
 */
function showToast(message, type = 'info') {
    // 创建Toast容器（如果不存在）
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // 创建Toast元素
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);

    // 显示Toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    toast.show();

    // 移除已隐藏的Toast
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * AJAX请求封装
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise} 返回Promise对象
 */
function ajaxRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    const finalOptions = { ...defaultOptions, ...options };

    return fetch(url, finalOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('AJAX请求错误:', error);
            showToast('请求失败，请稍后重试', 'error');
            throw error;
        });
}

/**
 * 刷新页面数据
 * @param {number} interval - 刷新间隔（毫秒）
 */
function startAutoRefresh(interval = 30000) {
    setInterval(function() {
        // 检查页面是否可见
        if (!document.hidden) {
            location.reload();
        }
    }, interval);
}

/**
 * 导出函数到全局作用域
 */
window.utils = {
    formatDateTime,
    confirmAction,
    showLoading,
    copyToClipboard,
    showToast,
    ajaxRequest,
    startAutoRefresh
};