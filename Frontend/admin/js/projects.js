document.addEventListener("DOMContentLoaded", () => {
    const openModalButton = document.getElementById("open-project-modal");
    const closeModalButton = document.getElementById("close-project-modal");
    const modal = document.getElementById("project-modal");
    const projectForm = document.getElementById("project-form");
    const projectIdField = document.getElementById("project-id");
    const modalTitle = document.getElementById("modal-title");

    const openModal = () => modal.classList.add("open");
    const closeModal = () => {
        modal.classList.remove("open");
        projectForm.reset();
        projectIdField.value = "";
        modalTitle.textContent = "Tambah Proyek";
        projectForm.action = "/projects/add";
    };

    openModalButton?.addEventListener("click", openModal);
    closeModalButton?.addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    document.querySelectorAll(".edit-project").forEach((button) => {
        button.addEventListener("click", () => {
            const projectId = button.dataset.id;
            const judul = button.dataset.judul;
            const deskripsi = button.dataset.deskripsi;
            const link = button.dataset.link;

            projectIdField.value = projectId;
            modalTitle.textContent = "Edit Proyek";
            projectForm.action = `/projects/${projectId}/edit`;
            projectForm.querySelector("#judul_proyek").value = judul;
            projectForm.querySelector("#deskripsi").value = deskripsi;
            projectForm.querySelector("#link_proyek").value = link;
            openModal();
        });
    });

    document.querySelectorAll("button[data-action='delete']").forEach((button) => {
        button.addEventListener("click", async () => {
            const projectId = button.dataset.id;
            const confirmed = confirm("Hapus proyek ini?");
            if (!confirmed) return;

            try {
                const response = await fetch(`/projects/${projectId}/delete`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                });
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Gagal menghapus proyek. Silakan coba lagi.");
                }
            } catch (error) {
                alert("Terjadi kesalahan saat menghapus proyek.");
            }
        });
    });
});
