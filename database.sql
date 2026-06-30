-- ============================================
-- DATABASE SCHEMA - PORTFOLIO PORTOFOLIO_TUGAS
-- Compatible dengan MySQL 5.7+ & TiDB
-- ============================================

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE portfolio_db;

-- ============================================
-- TABLE: admin
-- Purpose: Admin authentication & user management
-- ============================================
CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Admin ID',
    username VARCHAR(100) NOT NULL UNIQUE COMMENT 'Admin username untuk login',
    password VARCHAR(255) NOT NULL COMMENT 'Admin password (hashed)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan akun',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu update terakhir',
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (username: admin, password: admin123)
-- Password hash menggunakan SHA-256: echo -n "admin123" | sha256sum
INSERT INTO admin (username, password) VALUES ('admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

-- ============================================
-- TABLE: profil
-- Purpose: Profil portfolio pemilik
-- ============================================
CREATE TABLE IF NOT EXISTS profil (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Profil ID',
    nama_lengkap VARCHAR(150) NOT NULL COMMENT 'Nama lengkap pemilik portfolio',
    jabatan VARCHAR(100) NOT NULL COMMENT 'Jabatan/posisi saat ini',
    bio TEXT COMMENT 'Biografi singkat',
    foto_url VARCHAR(500) COMMENT 'URL foto profil dari Cloudinary atau CDN',
    link_github VARCHAR(255) COMMENT 'Link GitHub profile',
    link_linkedin VARCHAR(255) COMMENT 'Link LinkedIn profile',
    link_instagram VARCHAR(255) COMMENT 'Link Instagram profile',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu update terakhir',
    INDEX idx_nama (nama_lengkap),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: skill
-- Purpose: Technical skills & expertise
-- ============================================
CREATE TABLE IF NOT EXISTS skill (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Skill ID',
    nama_skill VARCHAR(100) NOT NULL COMMENT 'Nama skill/teknologi (misal: Python, React, Docker)',
    kategori_skill VARCHAR(100) NOT NULL COMMENT 'Kategori skill (misal: Backend, Frontend, DevOps)',
    persentase_keahlian INT DEFAULT 50 COMMENT 'Tingkat keahlian dalam persen (0-100)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu update terakhir',
    INDEX idx_kategori (kategori_skill),
    INDEX idx_nama (nama_skill),
    INDEX idx_persentase (persentase_keahlian)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: pengalaman
-- Purpose: Work experience & employment history
-- ============================================
CREATE TABLE IF NOT EXISTS pengalaman (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Pengalaman ID',
    posisi VARCHAR(150) NOT NULL COMMENT 'Posisi/jabatan yang dijalani (misal: Junior Developer)',
    nama_instansi VARCHAR(200) NOT NULL COMMENT 'Nama perusahaan/organisasi tempat bekerja',
    tanggal_mulai DATE NOT NULL COMMENT 'Tanggal mulai bekerja',
    tanggal_selesai DATE COMMENT 'Tanggal selesai bekerja (NULL jika masih bekerja)',
    deskripsi_tugas TEXT COMMENT 'Deskripsi pekerjaan dan pencapaian',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu update terakhir',
    INDEX idx_posisi (posisi),
    INDEX idx_instansi (nama_instansi),
    INDEX idx_tanggal (tanggal_mulai)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: proyek
-- Purpose: Portfolio projects showcase
-- ============================================
CREATE TABLE IF NOT EXISTS proyek (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Proyek ID',
    judul_proyek VARCHAR(255) NOT NULL COMMENT 'Judul/nama proyek',
    deskripsi TEXT COMMENT 'Deskripsi lengkap proyek dan fitur-fiturnya',
    gambar_url VARCHAR(500) COMMENT 'URL gambar/screenshot proyek dari Cloudinary',
    link_proyek VARCHAR(255) COMMENT 'URL link menuju proyek (live demo atau repository)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu update terakhir',
    INDEX idx_judul (judul_proyek),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: kontak
-- Purpose: Contact messages from visitors
-- ============================================
CREATE TABLE IF NOT EXISTS kontak (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Kontak ID',
    nama_pengirim VARCHAR(150) NOT NULL COMMENT 'Nama pengirim pesan',
    email_pengirim VARCHAR(150) NOT NULL COMMENT 'Email pengirim untuk follow-up',
    subjek VARCHAR(255) NOT NULL COMMENT 'Subjek/topik pesan',
    isi_pesan TEXT NOT NULL COMMENT 'Isi/body pesan dari pengunjung',
    tanggal_kirim DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pesan dikirim',
    dibaca TINYINT DEFAULT 0 COMMENT 'Flag: 0=belum dibaca, 1=sudah dibaca',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu record pembuatan',
    INDEX idx_email (email_pengirim),
    INDEX idx_tanggal (tanggal_kirim),
    INDEX idx_dibaca (dibaca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- DATABASE SCHEMA COMPLETE
-- ============================================
-- Summary of tables:
-- 1. admin - Authentication & user management
-- 2. profil - Portfolio owner profile
-- 3. skill - Technical skills inventory
-- 4. pengalaman - Work experience history
-- 5. proyek - Portfolio projects
-- 6. kontak - Contact messages from visitors
-- ============================================
