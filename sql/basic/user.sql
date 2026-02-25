DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user {
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username varchar(64) NOT NULL COMMENT '用户名',
    phone varchar(64) NOT NULL COMMENT '手机号',
    role varchar(16) NOT NULL COMMENT 'comm-普通用户、vip-vip用户、admin-管理员',
    status TINYINT DEFAULT 1 COMMENT '1-激活,0-注销',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
    KEY idx_status (status),
    KEY idx_role (role)
} ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';