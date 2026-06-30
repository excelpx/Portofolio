from flask import Flask, jsonify
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

from config import active_config
from model import db
from Backend.admin.upload import initialize_cloudinary
from Backend.utama.email_service import initialize_resend
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.projects import projects_bp
from Backend.admin.skills import skills_bp
from Backend.admin.experience import experience_bp
from Backend.utama.utama import utama_bp

app = Flask(__name__, template_folder="Frontend", static_folder="Frontend")

app.config.from_object(active_config)

print("========== RAILWAY DEBUG ==========")
print("FLASK_ENV =", os.getenv("FLASK_ENV"))
print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_PORT =", os.getenv("DB_PORT"))
print("DB_USER =", os.getenv("DB_USER"))
print("DB_NAME =", os.getenv("DB_NAME"))
print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])
print("===================================")

db.init_app(app)

with app.app_context():
    cloudinary_status = initialize_cloudinary()
    resend_status = initialize_resend()
    enable_db_create = os.getenv("ENABLE_DB_CREATE", "0") in ("1", "true", "True")
    if enable_db_create:
        try:
            db.create_all()
            print("✓ Database tables synchronized successfully with TiDB Cloud!")
        except Exception as db_err:
            print(f"✗ Failed to synchronize database tables: {db_err}")
    else:
        print("i: Skipping automatic db.create_all(); set ENABLE_DB_CREATE=1 to enable")


@app.context_processor
def inject_now():
    """Injects datetime.utcnow() into all Jinja templates automatically"""
    return {'now': datetime.utcnow}


@app.route("/api", methods=["GET"])
def index():
    """Test route to verify Flask app is running"""
    return jsonify(
        {
            "message": "✓ Flask Portfolio App is running successfully!",
            "status": "healthy",
            "environment": app.config.get("FLASK_ENV", "development"),
            "database": "configured",
        }
    )


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "ok",
            "flask": "working",
            "database": "ready",
        }
    ), 200


@app.route("/api/database-status", methods=["GET"])
def database_status():
    """Check database connection status"""
    try:
        db.session.execute("SELECT 1")
        return jsonify(
            {
                "status": "connected",
                "message": "Database connection successful",
            }
        ), 200
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return jsonify(
            {
                "status": "disconnected",
                "message": f"Database error: {str(e)}",
            }
        ), 500


@app.route("/api/test-integrasi", methods=["GET"])
def test_integrasi():
    """
    Test route to verify third-party service integrations
    Tests Cloudinary and Resend API key configurations
    """
    try:
        cloudinary_config = {
            "status": "unconfigured",
            "cloud_name_set": bool(os.getenv("CLOUDINARY_CLOUD_NAME")),
            "api_key_set": bool(os.getenv("CLOUDINARY_API_KEY")),
            "api_secret_set": bool(os.getenv("CLOUDINARY_API_SECRET")),
        }
        
        if all([
            os.getenv("CLOUDINARY_CLOUD_NAME"),
            os.getenv("CLOUDINARY_API_KEY"),
            os.getenv("CLOUDINARY_API_SECRET")
        ]):
            cloudinary_config["status"] = "configured"
            cloudinary_config["initialized"] = cloudinary_status
        
        resend_config = {
            "status": "unconfigured",
            "api_key_set": bool(os.getenv("RESEND_API_KEY")),
            "admin_email_set": bool(os.getenv("ADMIN_EMAIL")),
        }
        
        if os.getenv("RESEND_API_KEY"):
            resend_config["status"] = "configured"
            resend_config["initialized"] = resend_status
        
        try:
            db.session.execute("SELECT 1")
            database_config = {
                "status": "connected",
                "message": "Database connection successful"
            }
        except Exception as e:
            database_config = {
                "status": "disconnected",
                "error": str(e)
            }
        
        return jsonify(
            {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "integrations": {
                    "cloudinary": cloudinary_config,
                    "resend": resend_config,
                    "database": database_config,
                },
                "message": "Integration test completed"
            }
        ), 200
    
    except Exception as e:
        logger.error(f"Integration test error: {e}")
        return jsonify(
            {
                "status": "error",
                "message": f"Integration test failed: {str(e)}"
            }
        ), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experience_bp)
app.register_blueprint(utama_bp)


if __name__ == "__main__":
    try:
        env = os.getenv("FLASK_ENV", "development")
        logger.info(f"Starting Flask app in {env} mode...")
        logger.info(f"Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        logger.info(f"Cloudinary: {'✓ Initialized' if cloudinary_status else '✗ Not initialized'}")
        logger.info(f"Resend: {'✓ Initialized' if resend_status else '✗ Not initialized'}")
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=app.config.get("DEBUG", False),
        )
    except Exception as e:
        logger.error(f"Error starting app: {e}")
        raise
