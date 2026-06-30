from flask import Blueprint, render_template, redirect, url_for, session
from model import Skill, Pengalaman, Proyek, Kontak

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@dashboard_bp.route("/admin/dashboard", methods=["GET"])
def dashboard():
    """Render admin dashboard if user is authenticated."""
    if not session.get("is_admin_authenticated"):
        return redirect(url_for("login_bp.login"))

    total_skill = Skill.query.count()
    total_pengalaman = Pengalaman.query.count()
    total_proyek = Proyek.query.count()
    total_kontak = Kontak.query.count()

    return render_template(
        "admin/dashboard.html",
        totals={
            "skill": total_skill,
            "pengalaman": total_pengalaman,
            "proyek": total_proyek,
            "kontak": total_kontak,
        },
    )
