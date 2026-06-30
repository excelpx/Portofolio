from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import db, Pengalaman

experience_bp = Blueprint("experience_bp", __name__)


@experience_bp.route("/pengalaman", methods=["GET"])
@experience_bp.route("/admin/pengalaman", methods=["GET"])
def list_experience():
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    pengalaman = Pengalaman.query.order_by(Pengalaman.id.asc()).all()
    return render_template("admin/experience.html", pengalaman=pengalaman)


@experience_bp.route("/pengalaman/add", methods=["POST"])
def add_experience():
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    posisi = request.form.get("posisi", "").strip()
    nama_instansi = request.form.get("nama_instansi", "").strip()
    tanggal_mulai = request.form.get("tanggal_mulai", "").strip()
    tanggal_selesai = request.form.get("tanggal_selesai", "").strip()
    deskripsi_tugas = request.form.get("deskripsi_tugas", "").strip()

    pengalaman = Pengalaman(
        posisi=posisi,
        nama_instansi=nama_instansi,
        tanggal_mulai=tanggal_mulai or None,
        tanggal_selesai=tanggal_selesai or None,
        deskripsi_tugas=deskripsi_tugas,
    )

    try:
        db.session.add(pengalaman)
        db.session.commit()
        flash("Pengalaman berhasil ditambahkan.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menambahkan pengalaman: {str(exc)}", "danger")

    return redirect(url_for("experience_bp.list_experience"))


@experience_bp.route("/pengalaman/<int:experience_id>/edit", methods=["POST"])
def update_experience(experience_id):
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    pengalaman = Pengalaman.query.get_or_404(experience_id)
    pengalaman.posisi = request.form.get("posisi", pengalaman.posisi).strip()
    pengalaman.nama_instansi = request.form.get("nama_instansi", pengalaman.nama_instansi).strip()
    pengalaman.tanggal_mulai = request.form.get("tanggal_mulai", pengalaman.tanggal_mulai)
    pengalaman.tanggal_selesai = request.form.get("tanggal_selesai", pengalaman.tanggal_selesai)
    pengalaman.deskripsi_tugas = request.form.get("deskripsi_tugas", pengalaman.deskripsi_tugas).strip()

    try:
        db.session.commit()
        flash("Pengalaman berhasil diperbarui.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal memperbarui pengalaman: {str(exc)}", "danger")

    return redirect(url_for("experience_bp.list_experience"))


@experience_bp.route("/pengalaman/<int:experience_id>/delete", methods=["POST"])
def delete_experience(experience_id):
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    pengalaman = Pengalaman.query.get_or_404(experience_id)
    try:
        db.session.delete(pengalaman)
        db.session.commit()
        flash("Pengalaman berhasil dihapus.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menghapus pengalaman: {str(exc)}", "danger")

    return redirect(url_for("experience_bp.list_experience"))
