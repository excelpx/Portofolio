"""
Flask-SQLAlchemy Models for Portfolio Application
All table names and column names match exactly with database.sql
Each model includes to_dict() method for JSON serialization
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Admin(db.Model):
    """
    Admin Model
    Table: admin
    Purpose: Admin authentication & user management
    """
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Admin ID")
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
        comment="Admin username untuk login"
    )
    password = db.Column(
        db.String(255),
        nullable=False,
        comment="Admin password (hashed)"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pembuatan akun"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Waktu update terakhir"
    )

    def __repr__(self):
        return f"<Admin {self.username}>"

    def to_dict(self):
        """Convert Admin object to dictionary for JSON response"""
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Profil(db.Model):
    """
    Profil Model
    Table: profil
    Purpose: Profil portfolio pemilik
    """
    __tablename__ = "profil"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Profil ID")
    nama_lengkap = db.Column(
        db.String(150),
        nullable=False,
        comment="Nama lengkap pemilik portfolio"
    )
    jabatan = db.Column(
        db.String(100),
        nullable=False,
        comment="Jabatan/posisi saat ini"
    )
    bio = db.Column(
        db.Text,
        nullable=True,
        comment="Biografi singkat"
    )
    foto_url = db.Column(
        db.String(500),
        nullable=True,
        comment="URL foto profil dari Cloudinary atau CDN"
    )
    link_github = db.Column(
        db.String(255),
        nullable=True,
        comment="Link GitHub profile"
    )
    link_linkedin = db.Column(
        db.String(255),
        nullable=True,
        comment="Link LinkedIn profile"
    )
    link_instagram = db.Column(
        db.String(255),
        nullable=True,
        comment="Link Instagram profile"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pembuatan"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Waktu update terakhir"
    )

    def __repr__(self):
        return f"<Profil {self.nama_lengkap}>"

    def to_dict(self):
        """Convert Profil object to dictionary for JSON response"""
        return {
            "id": self.id,
            "nama_lengkap": self.nama_lengkap,
            "jabatan": self.jabatan,
            "bio": self.bio,
            "foto_url": self.foto_url,
            "link_github": self.link_github,
            "link_linkedin": self.link_linkedin,
            "link_instagram": self.link_instagram,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Skill(db.Model):
    """
    Skill Model
    Table: skill
    Purpose: Technical skills & expertise
    """
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Skill ID")
    nama_skill = db.Column(
        db.String(100),
        nullable=False,
        comment="Nama skill/teknologi (misal: Python, React, Docker)"
    )
    kategori_skill = db.Column(
        db.String(100),
        nullable=False,
        comment="Kategori skill (misal: Backend, Frontend, DevOps)"
    )
    persentase_keahlian = db.Column(
        db.Integer,
        default=50,
        nullable=False,
        comment="Tingkat keahlian dalam persen (0-100)"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pembuatan"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Waktu update terakhir"
    )

    def __repr__(self):
        return f"<Skill {self.nama_skill} ({self.kategori_skill})>"

    def to_dict(self):
        """Convert Skill object to dictionary for JSON response"""
        return {
            "id": self.id,
            "nama_skill": self.nama_skill,
            "kategori_skill": self.kategori_skill,
            "persentase_keahlian": self.persentase_keahlian,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Pengalaman(db.Model):
    """
    Pengalaman Model
    Table: pengalaman
    Purpose: Work experience & employment history
    """
    __tablename__ = "pengalaman"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Pengalaman ID")
    posisi = db.Column(
        db.String(150),
        nullable=False,
        comment="Posisi/jabatan yang dijalani (misal: Junior Developer)"
    )
    nama_instansi = db.Column(
        db.String(200),
        nullable=False,
        comment="Nama perusahaan/organisasi tempat bekerja"
    )
    tanggal_mulai = db.Column(
        db.Date,
        nullable=False,
        comment="Tanggal mulai bekerja"
    )
    tanggal_selesai = db.Column(
        db.Date,
        nullable=True,
        comment="Tanggal selesai bekerja (NULL jika masih bekerja)"
    )
    deskripsi_tugas = db.Column(
        db.Text,
        nullable=True,
        comment="Deskripsi pekerjaan dan pencapaian"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pembuatan"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Waktu update terakhir"
    )

    def __repr__(self):
        return f"<Pengalaman {self.posisi} di {self.nama_instansi}>"

    def to_dict(self):
        """Convert Pengalaman object to dictionary for JSON response"""
        return {
            "id": self.id,
            "posisi": self.posisi,
            "nama_instansi": self.nama_instansi,
            "tanggal_mulai": self.tanggal_mulai.isoformat() if self.tanggal_mulai else None,
            "tanggal_selesai": self.tanggal_selesai.isoformat() if self.tanggal_selesai else None,
            "deskripsi_tugas": self.deskripsi_tugas,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Proyek(db.Model):
    """
    Proyek Model
    Table: proyek
    Purpose: Portfolio projects showcase
    """
    __tablename__ = "proyek"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Proyek ID")
    judul_proyek = db.Column(
        db.String(255),
        nullable=False,
        comment="Judul/nama proyek"
    )
    deskripsi = db.Column(
        db.Text,
        nullable=True,
        comment="Deskripsi lengkap proyek dan fitur-fiturnya"
    )
    gambar_url = db.Column(
        db.String(500),
        nullable=True,
        comment="URL gambar/screenshot proyek dari Cloudinary"
    )
    link_proyek = db.Column(
        db.String(255),
        nullable=True,
        comment="URL link menuju proyek (live demo atau repository)"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pembuatan"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Waktu update terakhir"
    )

    def __repr__(self):
        return f"<Proyek {self.judul_proyek}>"

    def to_dict(self):
        """Convert Proyek object to dictionary for JSON response"""
        return {
            "id": self.id,
            "judul_proyek": self.judul_proyek,
            "deskripsi": self.deskripsi,
            "gambar_url": self.gambar_url,
            "link_proyek": self.link_proyek,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Kontak(db.Model):
    """
    Kontak Model
    Table: kontak
    Purpose: Contact messages from visitors
    """
    __tablename__ = "kontak"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Kontak ID")
    nama_pengirim = db.Column(
        db.String(150),
        nullable=False,
        comment="Nama pengirim pesan"
    )
    email_pengirim = db.Column(
        db.String(150),
        nullable=False,
        comment="Email pengirim untuk follow-up"
    )
    subjek = db.Column(
        db.String(255),
        nullable=False,
        comment="Subjek/topik pesan"
    )
    isi_pesan = db.Column(
        db.Text,
        nullable=False,
        comment="Isi/body pesan dari pengunjung"
    )
    tanggal_kirim = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu pesan dikirim"
    )
    dibaca = db.Column(
        db.Integer,
        default=0,
        nullable=False,
        comment="Flag: 0=belum dibaca, 1=sudah dibaca"
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Waktu record pembuatan"
    )

    def __repr__(self):
        return f"<Kontak {self.nama_pengirim} ({self.email_pengirim})>"

    def to_dict(self):
        """Convert Kontak object to dictionary for JSON response"""
        return {
            "id": self.id,
            "nama_pengirim": self.nama_pengirim,
            "email_pengirim": self.email_pengirim,
            "subjek": self.subjek,
            "isi_pesan": self.isi_pesan,
            "tanggal_kirim": self.tanggal_kirim.isoformat() if self.tanggal_kirim else None,
            "dibaca": self.dibaca,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

