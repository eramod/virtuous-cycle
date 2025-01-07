import React, { ReactPortal } from "react";
import ReactDOM from "react-dom";

interface ModalWrapperProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export default function Modal({ isOpen, onClose, title, children }: ModalWrapperProps): ReactPortal | null {
  if (!isOpen) return null;

  // Render modal content into the #modal-root div
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>{title}</h2>
        <button onClick={onClose}>Close</button>
        {children}
      </div>
    </div>,
    document.getElementById("modal-root")!
  );
}