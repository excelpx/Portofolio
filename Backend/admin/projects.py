from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import db, Proyek
from Backend.admin.upload import upload_gambar

projects_bp = Blueprint("projects_bp", __name__)


@projects_bp.route("/projects", methods=["GET"])
def list_projects():
    """List all project records."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    projects = Proyek.query.order_by(Proyek.id.asc()).all()
    return render_template("admin/projects.html", projects=projects)


@projects_bp.route("/projects/add", methods=["POST"])
def add_project():
    """Create a new project record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    judul_proyek = request.form.get("judul_proyek", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()
    link_proyek = request.form.get("link_proyek", "").strip()
    gambar_file = request.files.get("gambar")

    gambar_url = None
    if gambar_file and gambar_file.filename:
        upload_result = upload_gambar(gambar_file, folder="portfolio/projects")
        if not upload_result["success"]:
            flash(upload_result["error"], "danger")
            return redirect(url_for("projects_bp.list_projects"))
        gambar_url = upload_result["secure_url"]

    proyek = Proyek(
        judul_proyek=judul_proyek,
        deskripsi=deskripsi,
        gambar_url=gambar_url,
        link_proyek=link_proyek,
    )

    try:
        db.session.add(proyek)
        db.session.commit()
        flash("Proyek berhasil ditambahkan.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menambahkan proyek: {str(exc)}", "danger")

    return redirect(url_for("projects_bp.list_projects"))


@projects_bp.route("/projects/<int:project_id>/edit", methods=["POST", "PUT"])
def update_project(project_id):
    """Update an existing project record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    proyek = Proyek.query.get_or_404(project_id)
    proyek.judul_proyek = request.form.get("judul_proyek", proyek.judul_proyek).strip()
    proyek.deskripsi = request.form.get("deskripsi", proyek.deskripsi).strip()
    proyek.link_proyek = request.form.get("link_proyek", proyek.link_proyek).strip()

    gambar_file = request.files.get("gambar")
    if gambar_file and gambar_file.filename:
        upload_result = upload_gambar(gambar_file, folder="portfolio/projects")
        if not upload_result["success"]:
            flash(upload_result["error"], "danger")
            return redirect(url_for("projects_bp.list_projects"))
        proyek.gambar_url = upload_result["secure_url"]

    try:
        db.session.commit()
        flash("Proyek berhasil diperbarui.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal memperbarui proyek: {str(exc)}", "danger")

    return redirect(url_for("projects_bp.list_projects"))


@projects_bp.route("/projects/<int:project_id>/delete", methods=["POST", "DELETE"])
def delete_project(project_id):
    """Delete a project record."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    proyek = Proyek.query.get_or_404(project_id)
    try:
        db.session.delete(proyek)
        db.session.commit()
        flash("Proyek berhasil dihapus.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menghapus proyek: {str(exc)}", "danger")

    return redirect(url_for("projects_bp.list_projects"))
