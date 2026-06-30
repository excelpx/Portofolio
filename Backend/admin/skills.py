from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import db, Skill

skills_bp = Blueprint("skills_bp", __name__)


@skills_bp.route("/skills", methods=["GET"])
@skills_bp.route("/admin/skills", methods=["GET"])
def list_skills():
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    skills = Skill.query.order_by(Skill.id.asc()).all()
    return render_template("admin/skills.html", skills=skills)


@skills_bp.route("/skills/add", methods=["POST"])
def add_skill():
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    nama_skill = request.form.get("nama_skill", "").strip()
    kategori_skill = request.form.get("kategori_skill", "").strip()
    persentase_keahlian = request.form.get("persentase_keahlian", "0").strip()

    try:
        persentase_keahlian = int(persentase_keahlian)
    except ValueError:
        persentase_keahlian = 0

    skill = Skill(
        nama_skill=nama_skill,
        kategori_skill=kategori_skill,
        persentase_keahlian=max(0, min(persentase_keahlian, 100)),
    )

    try:
        db.session.add(skill)
        db.session.commit()
        flash("Skill berhasil ditambahkan.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menambahkan skill: {str(exc)}", "danger")

    return redirect(url_for("skills_bp.list_skills"))


@skills_bp.route("/skills/<int:skill_id>/edit", methods=["POST"])
def update_skill(skill_id):
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    skill = Skill.query.get_or_404(skill_id)
    skill.nama_skill = request.form.get("nama_skill", skill.nama_skill).strip()
    skill.kategori_skill = request.form.get("kategori_skill", skill.kategori_skill).strip()
    persentase = request.form.get("persentase_keahlian", skill.persentase_keahlian)

    try:
        persentase = int(persentase)
    except ValueError:
        persentase = skill.persentase_keahlian

    skill.persentase_keahlian = max(0, min(persentase, 100))

    try:
        db.session.commit()
        flash("Skill berhasil diperbarui.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal memperbarui skill: {str(exc)}", "danger")

    return redirect(url_for("skills_bp.list_skills"))


@skills_bp.route("/skills/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    skill = Skill.query.get_or_404(skill_id)
    try:
        db.session.delete(skill)
        db.session.commit()
        flash("Skill berhasil dihapus.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Gagal menghapus skill: {str(exc)}", "danger")

    return redirect(url_for("skills_bp.list_skills"))
