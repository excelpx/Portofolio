from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import db, Profil
from Backend.admin.upload import upload_gambar

profiles_bp = Blueprint("profiles_bp", __name__)


def _require_admin():
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))


@profiles_bp.route("/profiles", methods=["GET"])
def list_profiles():
    """List all profile records."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    profiles = Profil.query.order_by(Profil.id.asc()).all()
    return render_template("admin/profiles.html", profiles=profiles)


@profiles_bp.route("/profiles/add", methods=["POST"])
def add_profile():
    """Create a new profile record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    nama_lengkap = request.form.get("nama_lengkap", "").strip()
    jabatan = request.form.get("jabatan", "").strip()
    bio = request.form.get("bio", "").strip()
    link_github = request.form.get("link_github", "").strip()
    link_linkedin = request.form.get("link_linkedin", "").strip()
    link_instagram = request.form.get("link_instagram", "").strip()
    foto_file = request.files.get("foto")

    foto_url = None
    if foto_file and foto_file.filename:
        upload_result = upload_gambar(foto_file, folder="portfolio/profiles")
        if not upload_result["success"]:
            flash(upload_result["error"], "danger")
            return redirect(url_for("profiles_bp.list_profiles"))
        foto_url = upload_result["secure_url"]

    profile = Profil(
        nama_lengkap=nama_lengkap,
        jabatan=jabatan,
        bio=bio,
        foto_url=foto_url,
        link_github=link_github,
        link_linkedin=link_linkedin,
        link_instagram=link_instagram,
    )

    try:
        db.session.add(profile)
        db.session.commit()
        flash("Profil berhasil ditambahkan.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menambahkan profil: {str(exc)}", "danger")

    return redirect(url_for("profiles_bp.list_profiles"))


@profiles_bp.route("/profiles/<int:profile_id>/edit", methods=["POST", "PUT"])
def update_profile(profile_id):
    """Update an existing profile record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    profile = Profil.query.get_or_404(profile_id)
    profile.nama_lengkap = request.form.get("nama_lengkap", profile.nama_lengkap).strip()
    profile.jabatan = request.form.get("jabatan", profile.jabatan).strip()
    profile.bio = request.form.get("bio", profile.bio).strip()
    profile.link_github = request.form.get("link_github", profile.link_github).strip()
    profile.link_linkedin = request.form.get("link_linkedin", profile.link_linkedin).strip()
    profile.link_instagram = request.form.get("link_instagram", profile.link_instagram).strip()

    foto_file = request.files.get("foto")
    if foto_file and foto_file.filename:
        upload_result = upload_gambar(foto_file, folder="portfolio/profiles")
        if not upload_result["success"]:
            flash(upload_result["error"], "danger")
            return redirect(url_for("profiles_bp.list_profiles"))
        profile.foto_url = upload_result["secure_url"]

    try:
        db.session.commit()
        flash("Profil berhasil diperbarui.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal memperbarui profil: {str(exc)}", "danger")

    return redirect(url_for("profiles_bp.list_profiles"))


@profiles_bp.route("/profiles/<int:profile_id>/delete", methods=["POST", "DELETE"])
def delete_profile(profile_id):
    """Delete a profile record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    profile = Profil.query.get_or_404(profile_id)
    try:
        db.session.delete(profile)
        db.session.commit()
        flash("Profil berhasil dihapus.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menghapus profil: {str(exc)}", "danger")

    return redirect(url_for("profiles_bp.list_profiles"))
