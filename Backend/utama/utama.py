from flask import Blueprint, render_template, request, redirect, url_for, flash
from model import db, Profil, Skill, Pengalaman, Proyek, Kontak
from Backend.utama.email_service import kirim_email_notifikasi

utama_bp = Blueprint("utama_bp", __name__)


@utama_bp.route("/", methods=["GET"])
def index():
    """Render public portfolio homepage."""
    profil_list = Profil.query.order_by(Profil.id.asc()).all()
    skill_list = Skill.query.order_by(Skill.id.asc()).all()
    pengalaman_list = Pengalaman.query.order_by(Pengalaman.id.asc()).all()
    proyek_list = Proyek.query.order_by(Proyek.id.asc()).all()

    return render_template(
        "utama/index.html",
        profil_list=profil_list,
        skill_list=skill_list,
        pengalaman_list=pengalaman_list,
        proyek_list=proyek_list,
    )


@utama_bp.route("/kontak", methods=["POST"])
def kontak():
    """Handle public contact form submissions."""
    nama_pengirim = request.form.get("nama_pengirim", "").strip()
    email_pengirim = request.form.get("email_pengirim", "").strip()
    subjek = request.form.get("subjek", "").strip()
    isi_pesan = request.form.get("isi_pesan", "").strip()

    if not nama_pengirim or not email_pengirim or not subjek or not isi_pesan:
        flash("Semua field kontak harus diisi.", "danger")
        return redirect(url_for("utama_bp.index"))

    kontak = Kontak(
        nama_pengirim=nama_pengirim,
        email_pengirim=email_pengirim,
        subjek=subjek,
        isi_pesan=isi_pesan,
    )

    try:
        db.session.add(kontak)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menyimpan pesan kontak: {str(exc)}", "danger")
        return redirect(url_for("utama_bp.index"))

    email_result = kirim_email_notifikasi(
        nama=nama_pengirim,
        email_pengirim=email_pengirim,
        subjek=subjek,
        pesan=isi_pesan,
    )

    if email_result.get("success"):
        flash("Pesan kontak berhasil dikirim dan disimpan.", "success")
    else:
        flash(
            f"Pesan tersimpan, tetapi email notifikasi gagal: {email_result.get('error', 'Unknown error')}",
            "warning",
        )

    return redirect(url_for("utama_bp.index"))
