document.addEventListener("DOMContentLoaded", () => {
    const openModalButton = document.getElementById("open-experience-modal");
    const closeModalButton = document.getElementById("close-experience-modal");
    const modal = document.getElementById("experience-modal");
    const experienceForm = document.getElementById("experience-form");
    const experienceIdField = document.getElementById("experience-id");
    const modalTitle = document.getElementById("experience-modal-title");

    const openModal = () => modal.classList.add("open");
    const closeModal = () => {
        modal.classList.remove("open");
        experienceForm.reset();
        experienceIdField.value = "";
        modalTitle.textContent = "Tambah Pengalaman";
        experienceForm.action = "/pengalaman/add";
    };

    openModalButton?.addEventListener("click", openModal);
    closeModalButton?.addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    document.querySelectorAll(".edit-experience").forEach((button) => {
        button.addEventListener("click", () => {
            const experienceId = button.dataset.id;
            const posisi = button.dataset.posisi;
            const instansi = button.dataset.instansi;
            const mulai = button.dataset.mulai;
            const selesai = button.dataset.selesai;
            const deskripsi = button.dataset.deskripsi;

            experienceIdField.value = experienceId;
            modalTitle.textContent = "Edit Pengalaman";
            experienceForm.action = `/pengalaman/${experienceId}/edit`;
            experienceForm.querySelector("#posisi").value = posisi;
            experienceForm.querySelector("#nama_instansi").value = instansi;
            experienceForm.querySelector("#tanggal_mulai").value = mulai;
            experienceForm.querySelector("#tanggal_selesai").value = selesai;
            experienceForm.querySelector("#deskripsi_tugas").value = deskripsi;
            openModal();
        });
    });

    document.querySelectorAll("button[data-action='delete']").forEach((button) => {
        button.addEventListener("click", async () => {
            const experienceId = button.dataset.id;
            const confirmed = confirm("Hapus pengalaman ini?");
            if (!confirmed) return;

            try {
                const response = await fetch(`/pengalaman/${experienceId}/delete`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                });
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Gagal menghapus pengalaman. Silakan coba lagi.");
                }
            } catch (error) {
                alert("Terjadi kesalahan saat menghapus pengalaman.");
            }
        });
    });
});