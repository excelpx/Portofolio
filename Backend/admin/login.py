from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import db, Admin

login_bp = Blueprint("login_bp", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
@login_bp.route("/admin", methods=["GET"])
@login_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    """Handle admin login page and form submission."""
    if session.get("is_admin_authenticated"):
        return redirect(url_for("dashboard_bp.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session["is_admin_authenticated"] = True
            session["admin_username"] = admin.username
            flash("Login berhasil.", "success")
            return redirect(url_for("dashboard_bp.dashboard"))

        flash("Username atau password salah.", "danger")

    return render_template("admin/login.html")


@login_bp.route("/logout", methods=["GET"])
@login_bp.route("/admin/logout", methods=["GET"])
def logout():
    """Clear admin session and redirect to login."""
    session.pop("is_admin_authenticated", None)
    session.pop("admin_username", None)
    flash("Anda telah logout.", "info")
    return redirect(url_for("login_bp.login"))
