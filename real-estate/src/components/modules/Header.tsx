import Link from "next/link";
import styles from "@/components/modules/Header.module.css";
export default function Header() {
  return (
    <div className={styles.container}>
      <div className={styles.left}>
        <Link href="/">Home Page</Link>
        <Link href="/adver">Advertisements</Link>
      </div>
      <div className={styles.right}>
        <div className={styles.login}>
          <Link href="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}
