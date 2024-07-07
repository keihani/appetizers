import React from "react";
import styles from "@/components/modules/Footer.module.css";
import Link from "next/link";
export default function Footer() {
  return (
    <div className={styles.container}>
      <div className={styles.left}>
        <ul>
          <li>
            <Link href="/buy-residential">Advertisements</Link>
          </li>
          <li>
            <Link href="/create-residential">Ad Registration</Link>
          </li>
          <li>
            <Link href="/about-us">About us...</Link>
          </li>
        </ul>
      </div>
      <div className={styles.right}>
        <p>
          Address: Germany, Berlin <br />
          Tel: +49555555555
        </p>
      </div>
    </div>
  );
}
